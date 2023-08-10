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
//高度一樣
$(function(){
  var h = 0;

  $(".owl_main .item").each(function(){

    if($(this).height() > h){
      h = $(this).height();
    }
    
  });

  $(".owl_main .item").css("height",h + "px");
});


//

$(document).ready(function() {
  var carousel = $('#myCarousel .carousel-inner');
  var items = carousel.find('.carousel-item');
  var itemCount = items.length;
  var currentPage = 0;

  function showPage(page) {
    carousel.find('.carousel-item').removeClass('active');
    var numItemsToShow = getNumItemsToShow();
    items.slice(page, page + numItemsToShow).addClass('active');
  }

  function getNumItemsToShow() {
    var windowWidth = $(window).width();
    if (windowWidth < 576) {
      return 1;
    } else if (windowWidth < 768) {
      return 2;
    } else {
      return 4;
    }
  }

  // Initial setup
  showPage(currentPage);

  $(".carousel-control-prev").click(function() {
    currentPage = (currentPage - getNumItemsToShow() + itemCount) % itemCount;
    showPage(currentPage);
  });

  $(".carousel-control-next").click(function() {
    currentPage = (currentPage + getNumItemsToShow()) % itemCount;
    showPage(currentPage);
  });

  // Update carousel items on window resize
  $(window).resize(function() {
    showPage(currentPage);
  });
});



//輪播
$('.owl-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    dots:false,
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



//熱門行程詳細資訊
$(function(){
  $("#hot_spot_show").hide();

  $(".more_data").click(function(){

    $("#hot_spot_show").fadeIn(200);
  })

  $(".close").click(function(){
    $("#hot_spot_show").fadeOut(200);
  })
})

//add選單
function toggleDropdownMenu(addIcon) {
  var group = addIcon.closest('.group'); // 找到包含 addIcon 的最近的 .group 容器
  var dropdownMenu = group.find('.dropdown_menu'); // 使用 jQuery 的 find() 方法尋找 .dropdown_menu 元素
  var flagAdd = true;

  addIcon.onclick = function() {
    if (flagAdd) {
      flagAdd = false;
      dropdownMenu.fadeIn(200); 
      } else {
      flagAdd = true;
      dropdownMenu.fadeOut(200);
    }
  };
}

$(function() {
  $(".dropdown_menu").hide();

  $(".add_icon").click(function() {
    var addIcon = $(this);
    var dropdownMenu = addIcon.siblings(".dropdown_menu");

    // 如果 .dropdown_menu 是可見的，則點擊 .add_icon 會隱藏它，否則顯示它
    dropdownMenu.fadeToggle(200);
    addIcon.toggleClass("active");
  });

  // 點選任意地方時，檢查點擊的目標元素是否位於 .group 內部，若不是則隱藏 .dropdown_menu
  $(document).click(function(event) {
    if (!$(event.target).closest(".group").length) {
      $(".dropdown_menu").fadeOut(200);
      $(".add_icon").removeClass("active");
    }
  });
});
