$(document).ready(function(){
  $("#advertiser").chosen();
  $("#market").chosen();
  $("#device").chosen();
  var selects = $(".chosen-control").find("select");
  for (var i =0; i<selects.length; i++){
    $(selects[i]).chosen();
  }
  $(".chosen-input-search").chosen();
  var element = $("#scroll-data").attr("data");
  var scroll_element = '#' + element;
  try{
    $('html, body').animate({
        scrollTop: $(scroll_element).offset().top
    }, 100);
  }
  catch(err) {
    console.log(err);
  }
});
