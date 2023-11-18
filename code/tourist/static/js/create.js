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

//點了不會有空白 
function saveTabState(tabId, day) {
  var tabs = document.getElementsByClassName('tab-pane');
  for (var i = 0; i < tabs.length; i++) {
    tabs[i].style.display = 'none';
  }

  var tab = document.getElementById(tabId);
  tab.style.display = 'block';

  globalDay = day;
  console.log(globalDay);
  console.log(now_click_attractions);
  //使下面暫存的景點跟著換
  inputBottom();
  checkHasLocationData();
}


// 高度一致
$(document).ready(function () {
  // 在文件載入時和視窗尺寸改變時調整高度
  adjustTextHeightOnResize('.checkimg_div .spottxtdiv');
  adjustTextHeightOnResize('.S_checkimg_div .spottxtdiv');
});

function adjustTextHeightOnResize(selector) {
  // 初始化高度
  adjustTextHeight(selector);

  // 監聽視窗大小改變事件
  $(window).on('resize', function () {
    adjustTextHeight(selector);
  });
}

function adjustTextHeight(selector) {
  $(selector).height('auto'); // 先重置高度以便重新計算
  var maxHeight = 0;

  // 找出最大高度
  $(selector).each(function () {
    var textHeight = $(this).outerHeight();
    if (textHeight > maxHeight) {
      maxHeight = textHeight;
    }
  });

  // 將所有文字區塊設置為最大高度
  $(selector).height(maxHeight);
}

// 翻轉左邊區塊W&按鈕RWD變換

var total_day = document.getElementsByClassName('tab-pane')
var isdoneJourneyVisible = {};
for (var i = 0; i < total_day.length; i++) {
  isdoneJourneyVisible[i + 1] = false;
}

let isDoneVisible = false;

function flipped() {
  const done = document.getElementById('done-' + globalDay);
  const initialLayout = document.getElementById('initialLayout-'+globalDay);
  const flippedBtn = document.getElementById('flippedBtn-' + globalDay);

  if (isDoneVisible) {
    done.classList.remove('changeActive');
    setTimeout(() => {
      done.classList.add('hidden');
      initialLayout.classList.add('changeActive');
    }, 50); // 延遲切換，不然會直接跳轉沒有翻轉效果
    flippedBtn.textContent = '景點排序';
  } else {
    initialLayout.classList.remove('changeActive');
    done.classList.remove('hidden');
    setTimeout(() => {
      done.classList.add('changeActive');
    }, 50); 
    flippedBtn.textContent = '查看推薦';
  }
  isDoneVisible = !isDoneVisible;
}

// 送出功能整合到clickChangeDone函数中
// 點擊送出會切換到景點排序頁面
function submitNext(day) {
  showRightDiv();
}
function submitAction2(day) {
  console.log(3);
  if(!isDoneVisible){
    flipped();
  }
  showRightDiv();
  submitRecommend();
  // 隱藏 submitNext 按鈕
  var submitNextBtn = document.getElementById('submitNext-' + day);
  if (submitNextBtn) {
    submitNextBtn.classList.add('hideBtn');
  }
}


// 收合搜尋景點
var isopenSearchDivVisible = true;
function openSearchDiv() {
  var searchResult = $('.searchResult');
  isopenSearchDivVisible = !isopenSearchDivVisible

  if (isopenSearchDivVisible) {
    searchResult.animate({
      height: "show"
    }, 500);
  } else {
    searchResult.animate({
      height: "hide"
    }, 300);
  }
}

// 收合推薦
var isopenRecDivVisible = true;
function openRecDiv() {

  var openRec = $('.openRec');
  isopenRecDivVisible = !isopenRecDivVisible

  if (isopenRecDivVisible) {
    openRec.animate({
      height: "show"
    }, 500);
  } else {
    openRec.animate({
      height: "hide"
    }, 300);
  }
}

// 收合收藏
var isopenFavDivVisible = true;
function openFavDiv() {

  var openFav = $('.openFav');
  isopenFavDivVisible = !isopenFavDivVisible

  if (isopenFavDivVisible) {
    openFav.animate({
      height: "show"
    }, 500);
  } else {
    openFav.animate({
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

// pick spot css 點擊景點時
function pickspot(checkbox, aid) {
  console.log(checkbox);
  
  if (checkbox.classList.contains("pickimg")) {
    checkbox.classList.remove("pickimg");
    now_click_attractions[globalDay].delete(aid);
    inputBottom();
  } else {
    checkbox.classList.add("pickimg");
    now_click_attractions[globalDay].add(aid);
    inputBottom();
  }
}

// pick spot 刪除下面戰存的景點時
function pickspotBottom(aid) {
  try {
    const container = document.getElementById('ch-' + globalDay);
    const elements = container.querySelector('.imgcheck[value="' + aid + '"]');
    console.log(elements);
    pickspot(elements, aid);
  } catch (e) {
    now_click_attractions[globalDay].delete(aid);
    inputBottom();
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

function clickeInfo(event, itemId) {
  event.stopPropagation();
  // 這裡這裡的itemId要用你們的編號
  var S_info_icon = $("#" + itemId).find(".info_icon"); // 取得Info_icon按鈕

  if (!S_info_icon.hasClass("info_active")) {
    S_info_icon.addClass("info_active");
  } else {
    S_info_icon.removeClass("info_active");
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

// RWD縮小之後"儲存"變圖案
const saveBtn = document.querySelector('.recommend_save');

function changeBtnTxt() {
  if (window.innerWidth <= 690) {
    saveBtn.classList.add('saveIcon_btn');
    saveBtn.innerHTML = '';
  } else {
    saveBtn.classList.remove('saveIcon_btn');
    saveBtn.innerHTML = '儲存';
  }
}
window.onload = changeBtnTxt;
window.addEventListener('resize', changeBtnTxt);


// 定义一个函数来检查全局变量并更新CSS类
function checkAndAddClass() {
  var checkboxes = document.querySelectorAll('label[type="checkbox"]');
  checkboxes.forEach(function (checkbox) {
    var id = parseInt(checkbox.getAttribute('value'));
    console.log(globalDay);
    // 如果全局变量中包含 id，添加CSS类
    if (now_click_attractions[globalDay].has(id)) {
      var closestColMd6 = checkbox.closest('.col-md-6');
      var closestColMd4 = checkbox.closest('.col-md-4');
      // 添加额外的检查，确保 closestColMd6 存在
      if (closestColMd6) {
        closestColMd6.classList.add('pickimg');
      } else if (closestColMd4) {
        closestColMd4.classList.add('pickimg');
      }

    }
  });
}


function inputBottom(day = null) {
  if (day === null) {
    day = globalDay;
  }
  $.ajax({
    url: "/attractions",
    type: "GET",
    data: {
      aidlist: Array.from(now_click_attractions[day]).join(','),
    },
    success: function (response) {
      document.getElementById('bottomAttraction').innerHTML = response;
    },

    error: function () {
      console.log('推薦回傳有錯誤!!!');
    },
  });
}
// 用來進去翻轉景點排序或推薦景點的部分
function checkHasData() {
  const leftDev = document.querySelectorAll(".recAndDone");
  console.log(leftDev);
  leftDev.forEach(function (container, index) {
    const hasAttractions = container.querySelector('.innerlist');
    // console.log(hasAttractions);
    if (hasAttractions != null) {
      const changeToDone = container.querySelector('.changeToDone').id;
      clickChangeDone(changeToDone.charAt(changeToDone.length - 1))
    }
  });
}

function checkHasLocationData() {
  const location = document.querySelectorAll(".hiddenUserLocation");
  console.log(location);
  location.forEach(function (container, index) {
    // console.log(hasAttractions);
    if (container.value != ',') {
      startRecommend(container.value, index)
    }
  });
}

//用來把有的資料放入暫存區
function checkHasDataBottom() {

}

checkHasDataBottom()
window.onload = changeRepeatBtnTxt;
window.addEventListener('resize', changeRepeatBtnTxt);

