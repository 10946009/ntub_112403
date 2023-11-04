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

function saveTabState(tabId) {
  var tabs = document.getElementsByClassName('tab-pane');
  for (var i = 0; i < tabs.length; i++) {
      tabs[i].style.display = 'none';
  }

  var tab = document.getElementById(tabId);
  tab.style.display = 'block';
}

// 翻轉右邊區塊
var islikeAndRecVisible = false;

function clickChange() {
    const likeAndRec = document.getElementById('likeAndRec');
    const searchBlock = document.getElementById('searchBlock');
    const button = document.getElementById("changeToSearch");

    islikeAndRecVisible = !islikeAndRecVisible

    if (islikeAndRecVisible) {
        likeAndRec.style.transform = 'rotateY(180deg)';
        searchBlock.style.transform = 'rotateY(0deg)';
        button.textContent = "收藏與推薦";
        button.style.backgroundColor = "rgb(255, 41, 101)";
    } else {
        likeAndRec.style.transform = 'rotateY(0deg)';
        searchBlock.style.transform = 'rotateY(180deg)';
        button.textContent = "切換搜尋";
        button.style.backgroundColor = "#0066DB";
    }

}

// 翻轉左邊區塊
var isdoneJourneyVisible = false;

function clickChangeDone() {
    const checkRec = document.getElementById('checkRec');
    const done = document.getElementById('done');
    const button = document.getElementById("changeToRec");

    isdoneJourneyVisible = !isdoneJourneyVisible

    if (isdoneJourneyVisible) {
        checkRec.style.transform = 'rotateY(180deg)';
        done.style.transform = 'rotateY(0deg)';
        button.textContent = "重新推薦";
        button.style.backgroundColor = "rgb(255, 41, 101)";
    } else {
        checkRec.style.transform = 'rotateY(0deg)';
        done.style.transform = 'rotateY(180deg)';
        button.textContent = "景點排序";
        button.style.backgroundColor = "#0066DB";
    }

}

// 送出功能整合到clickChangeDone函数中
// 點擊送出會切換到景點排序頁面
function submitAction() {
  const checkRec = document.getElementById('checkRec');
  const done = document.getElementById('done');
  const button = document.getElementById("changeToRec");

  checkRec.style.transform = 'rotateY(180deg)';
  done.style.transform = 'rotateY(0deg)';
  button.textContent = "重新推薦";
  button.style.backgroundColor = "rgb(255, 41, 101)";
  isdoneJourneyVisible = true;
}


// 展開收藏跟相似景點
var isLikeVisible = false;

function openLikeBtn() {

    var openlike = $('.openlike');

    isLikeVisible = !isLikeVisible

    if (isLikeVisible) {
        openlike.animate({
            height: "show"
        }, 500);
    } else {
        openlike.animate({
            height: "hide"
        }, 500);
    }
}

var isSimilarVisible = false;
function openSimilarBtn() {

    var openSimilar = $('.openSimilar');

    isSimilarVisible = !isSimilarVisible

    if (isSimilarVisible) {
      openSimilar.animate({
            height: "show"
        }, 500);
    } else {
      openSimilar.animate({
            height: "hide"
        }, 300);
    }
}
//open篩選
function openfiliter() {
  var showfiliter = document.querySelector(".show_filiter")
  if (showfiliter.style.display === "none" || showfiliter.style.display === "") {
    showfiliter.style.display = "block";
  } else {
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

// 加入收藏
function addFavorite(itemId) {
  var ss_heart_icon = $("#" + itemId).find(".ss_heart_icon");

  if (!ss_heart_icon.hasClass("heart_active")) {
      ss_heart_icon.addClass("heart_active");
  } else {
      ss_heart_icon.removeClass("heart_active");
  }
}

// 建立行程裡面的收藏
function addCtFavorite(itemId) {
  var ct_heart_icon = $("#" + itemId).find(".ct_heart_icon");

  if (!ct_heart_icon.hasClass("heart_active")) {
      ct_heart_icon.addClass("heart_active");
  } else {
      ct_heart_icon.removeClass("heart_active");
  }
}

function addRecFavorite(event,itemId) {
  event.stopPropagation();
  // 這裡這裡的itemId要用你們的編號
  var rec_heart_icon = $("#" + itemId).find(".rec_heart_icon"); // 获取点击的爱心按钮

  if (!rec_heart_icon.hasClass("heart_active")) {
    rec_heart_icon.addClass("heart_active");
  } else {
    rec_heart_icon.removeClass("heart_active");
  }
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

// 托拽
var list = document.querySelector('.list')
var currentLi
list.addEventListener('dragstart', (e) => {
  e.dataTransfer.effectAllowed = 'move'
  currentLi = e.target
  setTimeout(() => {
    currentLi.classList.add('moving')
  })
})

list.addEventListener('dragenter', (e) => {
  e.preventDefault()
  if (e.target === currentLi || e.target === list) {
    return
  }
  var liArray = Array.from(list.childNodes)
  var currentIndex = liArray.indexOf(currentLi)
  var targetindex = liArray.indexOf(e.target)

  if (currentIndex < targetindex) {

    list.insertBefore(currentLi, e.target.nextElementSibling)
  } else {

    list.insertBefore(currentLi, e.target)
  }
})
list.addEventListener('dragover', (e) => {
  e.preventDefault()
})
list.addEventListener('dragend', (e) => {
  currentLi.classList.remove('moving')
})
