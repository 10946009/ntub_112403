document.addEventListener('DOMContentLoaded', function () {
  const selectedTab = localStorage.getItem('selectedTab');
  if (selectedTab === 'contact') {
    // 先移除之前的 active 状态
    document.getElementById('home-tab').classList.remove('active');
    document.getElementById('home').classList.remove('show', 'active');

    // 添加 active 状态到 contact 选项卡
    document.getElementById('contact-tab').classList.add('active');
    document.getElementById('contact').classList.add('show', 'active');
  }
});

//open篩選
function openfiliter(){
  var showfiliter = document.querySelector(".show_filiter")
  if(showfiliter.style.display === "none" || showfiliter.style.display === ""){
    showfiliter.style.display = "block";
  }else{
    showfiliter.style.display = "none";
  }
}

// pick spot css
function pickspot(checkbox) {
  checkbox.checked = !checkbox.checked;
  var div = checkbox.parentElement.parentElement; // 取得包含checkbox的div
  if (checkbox.checked) {
    div.classList.add("pickimg"); 
  } else {
    div.classList.remove("pickimg"); 
  }
}


var heart = document.getElementsByClassName('heart_icon');
// var span = document.getElementsByClassName('count');
for (var i = 0; i < heart.length; i++) {
  // var count;
  (function (i) {
    var flag = true;//點擊收藏
    heart[i].onclick = function () {
      if (flag) {
        flag = false;//無收藏被點擊
        this.className = "fa-solid fa-heart heart_icon heart_active";
        // ++span[i].innerHTML;
      } else {
        flag = true//點擊取消收藏
        this.className = "fa-solid fa-heart heart_icon";
        // --span[i].innerHTML;
      }
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

var dialog, x;
window.onload = function () {
  dialog = document.getElementById("dialog");
  x = document.getElementById("x");
}
function showDialog() {
  dialog.style.display = "block";
}
function hideDialog() {
  dialog.style.display = "none";
}