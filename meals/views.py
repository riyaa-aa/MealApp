from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from meals import models as m
from meals import forms as f
import pytz
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.urls import reverse

# logging out breaks the whole thing lol

def get_user_info(user):
    user_info,created = m.UserInfo.objects.get_or_create(user=user) #Creating the user info object if it doesn't exist and then returning it.
    return user_info


def get_meal_time():
    utc_now = timezone.now()
    # This could be derived from a setting the user selects
    user_timezone = pytz.timezone('Etc/GMT+8')
    now = utc_now.astimezone(user_timezone)

    now = datetime.now() + timedelta(hours=8) #To set to the right time.

    today4am = now.replace(hour=4, minute=0, second=0, microsecond=0)
    today11am = now.replace(hour=11, minute=0, second=0, microsecond=0)
    today4pm = now.replace(hour=16, minute=0, second=0, microsecond=0)
    today11pm = now.replace(hour=23, minute=0, second=0, microsecond=0)

    meal_time = None
    if now <= today11am and now > today4am:
        meal_time = m.Meal.BREAKFAST
    elif now > today11am and now <= today4pm:
        meal_time = m.Meal.LUNCH
    elif now > today4pm and now <= today11pm:
        meal_time = m.Meal.DINNER

    return meal_time

def get_filtered_meals(meals, restriction_ids):
    for id in restriction_ids:
        meals = meals.filter(restrictions__id=id)
    return meals

def get_current_meal(user_info, randomize):
    user_restriction_ids = user_info.restrictions.values_list("pk",flat=True)
    meals = m.Meal.objects.all()

    meals = get_filtered_meals(meals, user_restriction_ids)

    meal_time = get_meal_time()

    # If we within a part of the day with a set meal time, filter meals
    # for that meal time
    if meal_time:
        time_filter = {meal_time: True}
        meals = meals.filter(**time_filter)

    last_meal = None

    if randomize:
        meals = meals.order_by("?") #Order meals randomly
    else:
        meals = meals.order_by("pk") #Order meals by id
        # Find the last meal the user viewed
        if user_info and user_info.lastMeal: 
            last_meal = meals.filter(pk=user_info.lastMeal.pk).first()

    # If the meal time of the last meal does not match the current meal time,
    # do not use last meal.
    if last_meal and not getattr(last_meal, meal_time):
        last_meal = None  

    if last_meal:
        this_meal = last_meal
    else:
        this_meal = meals.first() #taking the first meal in the variable 'meals' (if last meal exists, it will be the only meal in 'meals')

    user_info.lastMeal = this_meal #the first meal in 'meals' will be the meal displayed, i.e. the one that needs to be stored to come back to.
    user_info.save()

    return this_meal


@login_required
def redirect_to_specific_meal(request):
    user_info = get_user_info(request.user)
    randomize = request.GET.get("randomize") #Query string
    meal = get_current_meal(user_info, randomize)

    url = reverse('home')
    return redirect("{}?meal_pk={}".format(url, meal.pk))


@login_required    
def home_view(request):
    # Shows a single meal based

    meal_pk = request.GET.get("meal_pk")

    # Home view should only ever be called for a specific meal
    if not meal_pk:
        return redirect(reverse("redirect_to_specific_meal"))

    print(meal_pk)
    this_meal = m.Meal.objects.get(pk=meal_pk)

    meal_time = get_meal_time()
    slogan = m.Meal.get_slogan(meal_time)

    #testing migration file
    ingredients_list = m.Meal.objects.values_list('ingredients')

    my_context = {
        "thisMeal": this_meal,
        "slogan": slogan,
        "ingList": ingredients_list,
    }
    
    return render(request, "home.html", my_context)


@login_required 
def weight_view(request):
    weights = m.Weight.objects.filter(user=request.user).order_by('date')
    todays_date = timezone.now().date()
    todays_weight = m.Weight.objects.filter(user=request.user, date=todays_date).first()
    form = f.WeightTracker(instance=todays_weight)

    weight_chart_data = []
    # If there is at least one weight entry, create chart data
    if weights.count() > 0:
        first_day = weights.first().date
        last_day = weights.last().date
        # Find the total number of days in the data span
        days = (last_day - first_day).days
        # Keep a running index in the weight data, since it may not exist in every day
        weight_index = 0
        # Loop over the range of days, inclusive
        for days_index in range(days + 1):
            weight_obj = weights[weight_index]
            weight_day = (weight_obj.date-first_day).days
            # If the current day corresponds to the next weight, enter this weight in the chart data
            if weight_day == days_index:
                weight = weight_obj.weight
                weight_index += 1
            else:
                # If there is no weight data for this day, put a None value for weight.
                # This will be converted to null in the template so chartjs ignores the value.
                weight = None
            data_element = {
                'date': days_index,
                'weight': weight,
            }
            weight_chart_data.append(data_element)
    print(weight_chart_data)

    if request.method == "POST":
        form = f.WeightTracker(request.POST, instance=todays_weight)
            # code for making them able to edit the date?
        if form.is_valid():
            user_weight = form.save(commit=False)
            user_weight.user = request.user
            user_weight.save()
            return redirect('weight')

            # make this form look like the settings one
            # when trying to decide if there is an instance of weight there needs to be filter for current user & day
            # get instance if it exists
        
    my_context = {
        "form": form, 
        "weights": weights,
        "todays_weight": todays_weight,
        "weight_chart_data":weight_chart_data,
    }
    return render(request, "weight.html", my_context)


@login_required 
def ingredients_add(request, id):
    savedMeal = get_object_or_404(m.Meal, id=id)
    if savedMeal.saved.filter(id=request.user.id).exists():
        savedMeal.saved.remove(request.user)
    else:
        savedMeal.saved.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required 
def ingredients_view(request):
    saved_meals = m.Meal.objects.filter(saved=request.user)
    meal_ingredients = []
    for meal in saved_meals:
        meal.generate_user_ingredients(request.user)
        user_ingredients = m.UserIngredient.objects.filter(user=request.user, ingredient__meal=meal, status=m.UserIngredient.STATUS_NEW)
        meal_ingredients.append(user_ingredients)
    num_saved = saved_meals.count()
    my_context={"new":saved_meals, "numSaved":num_saved, "mealIng":meal_ingredients}
    return render(request, "ingredients.html", my_context)


@login_required 
def favorites_add(request, id):
    favedMeal = get_object_or_404(m.Meal, id=id)
    if favedMeal.favorited.filter(id=request.user.id).exists():
        favedMeal.favorited.remove(request.user)
    else:
        favedMeal.favorited.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required 
def favorites_view(request):
    new = m.Meal.objects.filter(favorited=request.user)
    form = f.Restrictions(request.GET)
    restriction_ids = request.GET.getlist("restrictions")
    
    sort_form = f.SortBy(request.GET)
    sort_by = request.GET.get("sort_by")
    if sort_by:
        new = new.order_by(sort_by)

    new = get_filtered_meals(new, restriction_ids)

    numFaves = new.count()

    my_context={"new":new, "numFaves":numFaves, "form":form, "sort_form":sort_form}
    return render(request, "favorites.html", my_context)


@user_passes_test(m.check_admin) 
def browseMeals_view(response):
    meals = m.Meal.objects.all()
    count = 2
    my_context = {"meals":meals, "count":count}
    return render(response, "browse.html", my_context)


@login_required 
def meal_list_view(response, pk):
    mealObj = m.Meal.objects.get(id=pk)
    if m.Meal.objects.get(id=pk):
        nextmealObj = m.Meal.objects.get(id=pk)
        #nextmealObj = Meal.objects.get(id=pk+1)
    else:
        nextmealObj = m.Meal.objects.first()
    my_context={'mealObj':mealObj, 'nextMeal':nextmealObj}
    return render(response, "mealList.html", my_context)


@login_required 
def settings_view(request):
    form = f.Restrictions(instance=request.user.uInfo) # making sure that pre-saved restrictions appear
    if request.method == "POST":
        form = f.Restrictions(request.POST,instance=request.user.uInfo)
        if form.is_valid():
            user_info = form.save(commit=False) # prevents from saving to database since we don't know the user yet
            user_info.user = request.user
            user_info.save()
            form.save_m2m()
            return redirect('redirect_to_specific_meal')
        else:
            print("form isn't valid:", form.errors)
    my_context = {
        "form":form,
    }
    return render(request, "settings.html", my_context)


@login_required 
def navbar_view(request):
    new = m.Meal.objects.filter(favorited=request.user)
    numFaves = new.count()
    my_context={"numFaves":numFaves}
    return render(request, "base.html", my_context)
