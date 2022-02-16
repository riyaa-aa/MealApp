$(document).ready(function(){
  $('.expand_collapse_link').click(function() { // 'this' is the thing that is clicked on
      var link_element = $($(this)[0])
      var find_i = $(link_element.find("i")[0])
      if(link_element.attr("aria-expanded")=="true"){
        find_i.removeClass("fa-angle-down").addClass("fa-angle-up")
      }
      else{
        find_i.removeClass("fa-angle-up").addClass("fa-angle-down")
      }
  });
})