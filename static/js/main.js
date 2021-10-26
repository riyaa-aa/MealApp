var clicked = false;
$('.toggler').click(function() { 
    if (clicked == false) {
        $('div.vertical-nav').animate({
            'right': 0
        });
        clicked = true;

    }
    else {
        $('div.vertical-nav').animate({
            'right': -250
        });
        clicked = false;
    }
    $(this).toggleClass("far fa-heart fas fa-heart"); 
});

var select = function(s) {
    return document.querySelector(s);
  },
    icons = select('#icons'),
    button = select('.button'),
    buttonText = document.getElementById("button-text")
  
  // Morph the Download icon into the Checkmark icon
  var buttonTl = new TimelineMax({paused:true});
  buttonTl.to('#download', 1, {
    morphSVG:{shape:'#checkmark'},
    ease:Elastic.easeInOut
  })
  
  // On button click, play the animation
  button.addEventListener('click', function() {
    if (buttonTl.time() > 0) {
      buttonTl.reverse();
      
    } else {
      buttonTl.play(0);
    }
  })
  
  // On button click, swap out the button text
  button.addEventListener('click', function() {  
    if (button.classList.contains("saved")) {
      button.classList.remove("saved");
      buttonText.innerHTML = "Download";
    } else {
      button.classList.add("saved");
      buttonText.innerHTML = "Saved!";
    }
  }, false);