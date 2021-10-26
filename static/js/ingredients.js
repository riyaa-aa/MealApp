function update_ingredient(user_ingredient_id) {
    
    const formData = new FormData();

    formData.append('status', 'purchased');

    const csrf_token = document.querySelector('#ingredient_form input[name="csrfmiddlewaretoken"]')
    console.log("csrf_token", csrf_token)

    //formData.append('csrfmiddlewaretoken', csrf_token.value);
    console.log("formData", formData)

    fetch(`/api/user_ingredients/${user_ingredient_id}/`, {
        method: 'PUT',
        body: formData,
        headers: { "X-CSRFToken": csrf_token.value },
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}    

var ingredient_boxes = document.querySelectorAll(".ing_checkbox")
ingredient_boxes.forEach(element => {
    element.addEventListener("click", evt => {
        console.log("clicked")
        evt.target.parentElement.classList.add("invisible")
        var user_ingredient_id = evt.target.dataset.user_ingredient_id
        //target is the thing that is clicked --> can use this to access its data attributes
        //pass that value into update_ingredients
        update_ingredient(user_ingredient_id)
    })
});

