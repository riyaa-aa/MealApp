from django.db.models.fields.files import ImageField
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import *
from .forms import *
import random
import http
from datetime import datetime, timedelta
from django.http import HttpResponse, request
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Q

def get_user_info(user):
    user_info,created = UserInfo.objects.get_or_create(user=user) #Creating the user info object if it doesn't exist and then returning it.
    return user_info

def order_by_pk(arr, pk_arr):
    temp = 0
    sorted_pk = pk_arr
    sorted_arr = arr
    min_index = 0
    arr = arr
    pk_arr = pk_arr



    for i in range(len(pk_arr)):
        min_index = i
        for x in range(i+1, len(pk_arr)):
            if pk_arr[min_index] > pk_arr[x]:
                min_index = x
        temp = pk_arr[min_index]
        sorted_pk[min_index] = sorted_pk[i]
        sorted_pk[i] = temp
        #sorted_pk[i], sorted_pk[min_index] = sorted_pk[min_index], sorted_pk[i]

    test_arr=[]
    for j in range(len(sorted_pk)):
        for k in range(j,len(sorted_pk)):
            if sorted_pk[j] == pk_arr[k]:
                test_arr.append(2)
                temp = 2
                sorted_arr[j] = arr[k]
                #arr[j],arr[k] = arr[k],arr[j]

    return pk_arr

@login_required    
def home_view(request):

    randomize = request.GET.get("randomize") #Query string

    user_info = get_user_info(request.user)
    user_restriction_ids = user_info.restrictions.values_list("pk",flat=True)

    restriction_Q = Q()
    meals = Meal.objects.all()

    for id in user_restriction_ids:
        restriction_Q = restriction_Q & Q(restrictions__pk=id)
        meals = meals.filter(restrictions__id=id)

    # meals = Meal.objects.filter(restrictions__pk__in=user_restriction_ids).distinct()
    # meals = Meal.objects.filter(restriction_Q).distinct()
    print(meals)
    print(meals.query)

    # meal_count = meals.count()

    #test
    # meal_arr = []
    # pk_arr = []
    # first_meal = Meal.objects.first()
    # first_pk = first_meal.pk
    # str_meal_arr = ""
    
    # for i in range(meal_count):
    #     meal_arr.append(meals.get(pk=first_pk+i))
    #     pk_arr.append(first_pk+i)
    
    # str_meal_arr = ' '.join([str(item) for item in meal_arr])

    # test_arr = [3,6,2,8,4,9,1,10,5]
    # test_meals = ["this", "is", "a", "test", "to", "see", "if", "this", "works"]

    # get_ordered_pk = order_by_pk(test_meals,test_arr)
    #endtest

    #If the user exists and they have a last meal.
    last_meal = None

    if randomize:
        meals = meals.order_by("?") #Order meals randomly
    else:
        meals = meals.order_by("pk") #Order meals by id
        if user_info and user_info.lastMeal: 
            #meals = meals.filter(pk=user_info.lastMeal.pk) 
            print(meals)
            last_meal = meals.filter(pk=user_info.lastMeal.pk).first()
            print("gotit")
            print(last_meal)
        
    now = datetime.now() + timedelta(hours=8) #To set to the right time.

    today4am = now.replace(hour=4, minute=0, second=0, microsecond=0)
    today11am = now.replace(hour=11, minute=0, second=0, microsecond=0)
    today4pm = now.replace(hour=16, minute=0, second=0, microsecond=0)
    today11pm = now.replace(hour=23, minute=0, second=0, microsecond=0)

    slogan = ""

    if now <= today11am and now > today4am:
        meals = meals.filter(breakfast=True)
        slogan = "Your Breakfast:"
        if last_meal and not last_meal.breakfast:
            last_meal = None
    elif now > today11am and now <= today4pm:
        meals = meals.filter(lunch=True)
        slogan = "Your Lunch:"
        if last_meal and not last_meal.lunch:
            last_meal = None
    elif now > today4pm and now <= today11pm:
        meals = meals.filter(dinner=True)
        slogan = "Your Dinner:"
        if last_meal and not last_meal.dinner:
            last_meal = None
    else:
        slogan = "Go To Sleep!"

    if last_meal:
        this_meal=last_meal
    else:
        this_meal = meals.first() #taking the first meal in the variable 'meals' (if last meal exists, it will be the only meal in 'meals')

    user_info.lastMeal=this_meal #the first meal in 'meals' will be the meal displayed, i.e. the one that needs to be stored to come back to.
    user_info.save()

    #testing migration file
    ingredients_list = Meal.objects.values_list('ingredients')

    my_context = {
        "meals": meals, 
        "time": now, 
        "today4am": today4am,
        "thisMeal": this_meal,
        # "count":meal_count, 
        "slogan":slogan,
        "ingList":ingredients_list,
        # "test":str_meal_arr,
        # "test2":get_ordered_pk,
    }
    
    return render(request, "home.html", my_context)

@login_required 
def weight_view(response):
    weights = Weight.objects.all
    form = WeightTracker()

    if response.method == "POST":
        form = WeightTracker(response.POST)
        now = datetime.now() + timedelta(hours=8)
        if form.is_valid():
            n = form.cleaned_data["dailyweight"]
            #d = form.cleaned_data["dayTime"]
            #t = Weight(time=d)
            #for weight in weights:
                #if t.time == weight.time:
                    #y=0

            w = Weight(weight = n, time=now)
            w.save()
            response.user.weight.add(w)
            form = WeightTracker()
    else:
        form = WeightTracker()
        
    my_context = {"meals": Meal.objects.all, "form": form, "weights": weights}
    return render(response, "weight.html", my_context)

@login_required 
def ingredients_add(request, id):
    savedMeal = get_object_or_404(Meal, id=id)
    if savedMeal.saved.filter(id=request.user.id).exists():
        savedMeal.saved.remove(request.user)
    else:
        savedMeal.saved.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required 
def ingredients_view(request):
    saved_meals = Meal.objects.filter(saved=request.user)
    meal_ingredients = []
    for meal in saved_meals:
        meal.generate_user_ingredients(request.user)
        user_ingredients = UserIngredient.objects.filter(user=request.user, ingredient__meal=meal, status=UserIngredient.STATUS_NEW)
        meal_ingredients.append(user_ingredients)
    numSaved = saved_meals.count()
    my_context={"new":saved_meals, "numSaved":numSaved, "mealIng":meal_ingredients}
    return render(request, "ingredients.html", my_context)

def check(request):
    if 'checks[]' in request.GET:  #<----- 'checks[]'
      chosen = request.GET.getlist('checks[]')  #<----- 'checks[]'
      return render('home.html',{'chosen':chosen})
    else: 
        return render('home.html',{})

@login_required 
def favorites_add(request, id):
    favedMeal = get_object_or_404(Meal, id=id)
    if favedMeal.favorited.filter(id=request.user.id).exists():
        favedMeal.favorited.remove(request.user)
    else:
        favedMeal.favorited.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required 
def favorites_view(request):
    new = Meal.objects.filter(favorited=request.user)
    numFaves = new.count()
    my_context={"new":new, "numFaves":numFaves}
    return render(request, "favorites.html", my_context)

def check_admin(user):
    return user.is_superuser

@user_passes_test(check_admin) 
def browseMeals_view(response):
    meals = Meal.objects.all()
    count = 2
    my_context = {"meals":meals, "count":count}
    return render(response, "browse.html", my_context)

@login_required 
def meal_list_view(response, pk):
    mealObj = Meal.objects.get(id=pk)
    if Meal.objects.get(id=pk):
        nextmealObj = Meal.objects.get(id=pk)
        #nextmealObj = Meal.objects.get(id=pk+1)
    else:
        nextmealObj = Meal.objects.first()
    my_context={'mealObj':mealObj, 'nextMeal':nextmealObj}
    return render(response, "mealList.html", my_context)

@login_required 
def settings_view(response):
    form = Restrictions()
    if response.method == "POST":
        form = Restrictions(response.POST)
        if form.is_valid():
            n = form.cleaned_data["dietRestr"]
            r = Restrictions(dietRestr = n)
            r.save()
            response.user.dietRestr.add(r)
        else:
            form = Restrictions()
    my_context = {
        "form":form,
    }
    return render(response, "settings.html", my_context)

@login_required 
def navbar_view(request):
    new = Meal.objects.filter(favorited=request.user)
    numFaves = new.count()
    my_context={"numFaves":numFaves}
    return render(request, "base.html", my_context)