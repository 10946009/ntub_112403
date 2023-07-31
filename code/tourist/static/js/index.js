var heart = document.getElementsByClassName('heart_icon');
    // var span = document.getElementsByClassName('count');
    for(var i = 0;i < heart.length; i++){
        // var count;
        (function(i){
            var flag = true;//點擊收藏
            heart[i].onclick = function(){
                if(flag){
                    flag = false;//無收藏被點擊
                    this.className = "fa-solid fa-heart heart_icon active_heart";
                    // ++span[i].innerHTML;
                }else{
                    flag = true//點擊取消收藏
                    this.className = "fa-solid fa-heart heart_icon";
                    // --span[i].innerHTML;
                }
            }  
        })(i);
    } 
    
function add() {
    document.getElementsById("myDropdown").classList.toggle("show");
    }
      
    // Close the dropdown menu if the user clicks outside of it
    window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
              openDropdown.classList.remove('show');
            }
          }
        }
      }    
    
function add1() {
    document.getElementsById("myDropdown1").classList.toggle("show");
    }
      
    // Close the dropdown menu if the user clicks outside of it
    window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
              openDropdown.classList.remove('show');
            }
          }
        }
      }   

//漢堡選單
$(document).ready(function() {
   $('.showmenu').on('click',  function(e) {
      e.preventDefault();
      $('body').toggleClass('menu-show');
  });
});


$('.owl-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    // dots:false,
    responsive:{
        0:{
            items:2
        },
        600:{
            items:3
        },
        1000:{
            items:4
        }
    }
})

$(function(){
  $("#hot_spot_show").hide();

  $(".more_data").click(function(){

    $("#hot_spot_show").fadeIn(200);
  })

  $(".close").click(function(){
    $("#hot_spot_show").fadeOut(200);
  })
})

var add_click = document.getElementsByClassName('add_icon');
var count=1;
$(function(){
    $(".dropdown_menu").hide();
})
for(var i = 0 ; i < add_click.length ; i++){
  (function(i){
    var flag_add = true;
    add_click[i].onclick = function(){
      if(flag_add){
        flag_add = false//點add
        $(".dropdown_menu").fadeIn(200);
      }else{
        flag_add = true//點其他
        $(".dropdown_menu").fadeOut(200);
      }
      count++
    }
  })(i);
}

// $(function(){
//   $(".dropdown_menu").hide();
//   $(".add_icon").click(function(){
//     $(".dropdown_menu").fadeIn(200);
//   })
// })

  // if( count % 2 == 0 ){
  //   add_click[i].onclick = function(){
  //     $(".dropdown_menu").fadeOut(200);
  //   }
  // }else{
  //   $(".dropdown_menu").fadeIn(200);
  // }
  // count++;