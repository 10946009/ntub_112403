//圖片等於螢幕高度
window.onload = function () {
  var bannerbgimg = document.getElementsByClassName('banner');
  bannerbgimg.style.height = window.innerHeight + "px";
}
//重新計算螢幕高度
window.onresize = function () {
  var bannerbgimg = document.getElementsByClassName('banner');
  bannerbgimg.style.height = window.innerHeight + "px";
}

// randomBanner
document.addEventListener("DOMContentLoaded", function () {
  var images = [
    '../static/images/IMG20220125115200.jpg',
    '../static/images/bg1.jpg',
    '../static/images/bg2.jpg',
    '../static/images/bg5.png',
    '../static/images/bg6.jpeg',
    '../static/images/bg7.png',
    '../static/images/bg8.jpg',
    '../static/images/jp_img.jpg',
  ]

  var randomIndex = Math.floor(Math.random() * images.length);
  var randomImg = images[randomIndex];

  var banner = document.getElementById("randomBanner");

  banner.style.background = 'url(' + randomImg + ')';
  banner.style.backgroundRepeat = 'no-repeat';
  banner.style.backgroundSize = 'cover';
  banner.style.backgroundPosition = 'center';
  banner.style.opacity = '0.65';
  banner.style.position = 'relative';
  banner.style.zIndex = '100';
})

// change img when mouser hover
function startSlideshow(container) {
  let currentImageIndex = 1;  // 设置为1，从第二张图开始显示
  const images = container.querySelectorAll('.changeImg');

  // 显示下一张图（从第二张开始）
  images[currentImageIndex].classList.add('changeImg_show');

  // 启动定时器，每2秒切换一次图片
  container.slideshowInterval = setInterval(() => {
    images[currentImageIndex].classList.remove('changeImg_show');
    currentImageIndex = (currentImageIndex + 1) % images.length;
    images[currentImageIndex].classList.add('changeImg_show');
  }, 2000);
}

function stopSlideShow(container) {
  clearInterval(container.slideshowInterval);

  // 移除所有图片的 'show' 类
  container.querySelectorAll('.changeImg').forEach(img => img.classList.remove('changeImg_show'));

  // 将第一张图片添加 'show' 类
  container.querySelector('.changeImg').classList.add('changeImg_show');
}

//向下滑動
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
for (var i = 0; i < heart.length; i++) {
  // var count;
  (function (i) {
    heart[i].onclick = function () {
      var isFavorite = this.getAttribute("data-isfavorite");
      if (isFavorite === "0") {
        this.setAttribute("data-isfavorite", "1");//無收藏被點擊
        this.className = "fa-solid fa-heart heart_icon active_heart";
        // ++span[i].innerHTML;
      } else {
        this.setAttribute("data-isfavorite", "0");//點擊取消收藏
        this.className = "fa-solid fa-heart heart_icon";
        // --span[i].innerHTML;
      }
      id = this.getAttribute("data-id")
      type = this.getAttribute("data-type")
      addFavorite_index(id, type);
    }
  })(i);
}

//add選單
function toggleDropdownMenu(addIcon) {
  var group = addIcon.closest('.group'); // 找到包含 addIcon 的最近的 .group 容器
  var dropdownMenu = group.find('.dropdown_menu'); // 使用 jQuery 的 find() 方法尋找 .dropdown_menu 元素
  var flagAdd = true;

  addIcon.onclick = function () {
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
$(function () {
  $(".dropdown_menu").hide();

  $(".add_icon").click(function () {
    var addIcon = $(this);
    var dropdownMenu = addIcon.siblings(".dropdown_menu");

    // 如果 .dropdown_menu 是可見的，則點擊 .add_icon 會隱藏它，否則顯示它
    dropdownMenu.fadeToggle(200);
    addIcon.toggleClass("active");
  });

  // 點選任意地方時，檢查點擊的目標元素是否位於 .group 內部，若不是則隱藏 .dropdown_menu
  $(document).click(function (event) {
    if (!$(event.target).closest(".group").length) {
      $(".dropdown_menu").fadeOut(200);
      $(".add_icon").removeClass("active");
    }
  });
});

//滑到才顯示

$(document).ready(function () {
  /* Every time the window is scrolled ... */
  $(window).scroll(function () {
    /* Check the location of each desired element */

    // For .hideme
    $('.hideme').each(function (i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        $(this).animate({ 'opacity': '1' }, 500);
      }
    });

    // For .hidemespot
    $('.hidemespot').each(function (i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        $(this).animate({ 'opacity': '1' }, 1000);
      }
    });

    // For .hidemehot熱門景點
    $('.hidemehot').each(function (i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        setTimeout(function () {
          $this.css('position', 'relative');
          $this.css('top', '-100%');
          $this.animate({
            'opacity': '1',
            'top': '0'
          }, 1000); // 不同的延迟时间
        }, i * 500); // 不同的延迟时间
      }
    })

    // For .hidemehottoleft輪播
    $('.hidemehottoleft').each(function (i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        setTimeout(function () {
          $this.css('position', 'relative');
          $this.css('left', '100%');
          $this.animate({
            'opacity': '1',
            'left': '0'
          }, 1000); // 不同的延迟时间
        }, i * 500); // 不同的延迟时间
      }
    });

    // For .hidemeexplore
    $('.hidemeexplore').each(function (i) {
      var $this = $(this);
      var bottom_of_object = $this.offset().top + $this.outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if (bottom_of_window > bottom_of_object) {
        setTimeout(function () {
          $this.css('position', 'relative');
          $this.css('top', '100%');
          $this.animate({
            'opacity': '1',
            'top': '0'
          }, 1000); // 不同的延迟时间
        }, i * 500); // 不同的延迟时间
      }
    });
  });
});

// 高度一致
$(function () {
  var h = 0;
  $('.item .carousel_txt').each(function () {

    if ($(this).height() > h) {
      h = $(this).height();
    }

  });
  $('.item .carousel_txt').css('height', h + 'px');
});

