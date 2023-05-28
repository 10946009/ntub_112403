
$(function(){
  $('#contents section[id != "tab_c"]').hide();

  $("a").click(function(){
      $('#contents section').hide();

      $($(this).attr("href")).show();


      $(".current").removeClass("current");

      $(this).addClass("current");

      return false;
  });
});


var dialog,x;
window.onload=function(){
  dialog=document.getElementById("dialog");
  x=document.getElementById("x");
}
function showDialog(){
  dialog.style.display="block";
}
function hideDialog(){
  dialog.style.display="none";
}