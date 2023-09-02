//圖片等於螢幕高度
window.onload = function(){
  var bannerbgimg = document.getElementsByClassName('banner');
  bannerbgimg.style.height = window.innerHeight + "px";
}
//重新計算螢幕高度
window.onresize = function(){
  var bannerbgimg = document.getElementsByClassName('banner');
  bannerbgimg.style.height = window.innerHeight + "px";
}

//向下滑動
// document.querySelector('.scroll-down-button').addEventListener('click', function (e) {
//   e.preventDefault();
//   document.querySelector('#main').scrollIntoView({
//       behavior: 'smooth'
//   });
// });
document.querySelector('.scroll-down-button').addEventListener('click', function (e) {
  e.preventDefault();
  const navbarHeight = document.querySelector('nav').offsetHeight; // 获取导航栏的高度
  const targetElement = document.querySelector('#main');
  const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - navbarHeight;

  window.scrollTo({
    top: targetPosition,
    behavior: 'smooth'
  });
});

//收藏
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

//add dropdown
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

//滑到才顯示
// $(document).ready(function() {
//   /* Every time the window is scrolled ... */
//   $(window).scroll( function(){
//       /* Check the location of each desired element */
//       $('.hideme').each( function(i){
          
//           var bottom_of_object = $(this).offset().top + $(this).outerHeight();
//           var bottom_of_window = $(window).scrollTop() + $(window).height();
          
//           /* If the object is completely visible in the window, fade it it */
//           if( bottom_of_window > bottom_of_object ){
              
//               $(this).animate({'opacity':'1'},500);
//           }
//       }); 
//   });
// });

$(document).ready(function() {
  /* Every time the window is scrolled ... */
  $(window).scroll(function() {
    /* Check the location of each desired element */

    // For .hideme
    $('.hideme').each(function(i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        $(this).animate({'opacity':'1'},500);
      }
    });

    // For .hidemespot
    $('.hidemespot').each(function(i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        $(this).animate({'opacity':'1'},1000);
      }
    });

    // For .hidemehot
    $('.hidemehot').each(function(i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        setTimeout(function() {
          $this.animate({ 'opacity': '1' }, 1000); // 不同的延迟时间
        }, i * 500); // 不同的延迟时间
      }
    });
  });
});