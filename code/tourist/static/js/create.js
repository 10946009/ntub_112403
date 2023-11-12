
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
}

// 翻轉右邊區塊&按鈕RWD變換
var islikeAndRecVisible = false;
var isIconSet = false;

function checkWindowSize() {
  const button = document.getElementById('changeToSearch');
  if (window.innerWidth <= 690) {
    if (!isIconSet) {
      setIconContent(button);
      isIconSet = true;
    }
  } else {
    button.textContent = islikeAndRecVisible ? '收藏與推薦' : '切換搜尋';
    isIconSet = false;
  }
}
function setIconContent(button) {
  if (islikeAndRecVisible) {
    button.innerHTML = '<i class="fa-regular fa-face-grin-hearts"></i>';
  } else {
    button.innerHTML = '<i class="fa-solid fa-magnifying-glass-location"></i>';
  }
}
function rotateAndToggleContent() {
  const likeAndRec = document.getElementById('likeAndRec');
  const searchBlock = document.getElementById('searchBlock');
  const button = document.getElementById('changeToSearch');

  islikeAndRecVisible = !islikeAndRecVisible;

  if (islikeAndRecVisible) {
    likeAndRec.style.transform = 'rotateY(180deg)';
    searchBlock.style.transform = 'rotateY(0deg)';
    button.style.backgroundColor = 'rgb(255, 41, 101)';
    setIconContent(button);
    isIconSet = true;
  } else {
    likeAndRec.style.transform = 'rotateY(0deg)';
    searchBlock.style.transform = 'rotateY(180deg)';
    button.style.backgroundColor = '#0066DB';
    setIconContent(button);
    isIconSet = true;
  }
}

// Call checkWindowSize when the window loads and when it's resized
window.addEventListener('load', checkWindowSize);
window.addEventListener('resize', checkWindowSize);
// 被點的時候呼叫rotateAndToggleContent
document.getElementById('changeToSearch').addEventListener('click', rotateAndToggleContent);


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
// var isdoneJourneyVisible = false;
// var isLeftIconSet = false;

// function checkLeftWindowSize() {
//   const button = document.getElementsByClassName('changeToRec');
//   if (window.innerWidth <= 690) {
//     if (!isLeftIconSet) {
//       setLeftIconContent(button[0]); // Since getElementsByClassName returns a collection, select the first element
//       isLeftIconSet = true;
//     }
//   } else {
//     button[0].textContent = isdoneJourneyVisible ? '重新推薦' : '景點排序';
//     isLeftIconSet = false;
//   }
// }

// function setLeftIconContent(button) {
//   if (isdoneJourneyVisible) {
//     button.innerHTML = '<i class="fa-solid fa-repeat"></i>';
//   } else {
//     button.innerHTML = '<i class="fa-solid fa-route"></i>';
//   }
// }

// function rotateLeftAndToggleContent(globalDay) {
//   console.log(globalDay);
//   const checkRec = document.getElementById('checkRec-' + globalDay);
//   const done = document.getElementById('done-' + globalDay);
//   const button = document.getElementById("changeToRec-" + globalDay);

//   isdoneJourneyVisible = !isdoneJourneyVisible;

//   if (isdoneJourneyVisible) {
//     checkRec.style.transform = 'rotateY(180deg)';
//     done.style.transform = 'rotateY(0deg)';
//     button.style.backgroundColor = 'rgb(255, 41, 101)';
//     setLeftIconContent(button);
//     isLeftIconSet = true;
//   } else {
//     checkRec.style.transform = 'rotateY(0deg)';
//     done.style.transform = 'rotateY(180deg)';
//     button.style.backgroundColor = '#0066DB';
//     setLeftIconContent(button);
//     isLeftIconSet = true;
//   }
// }

// // Call checkLeftWindowSize when the window loads and when it's resized
// window.addEventListener('load', checkLeftWindowSize);
// window.addEventListener('resize', checkLeftWindowSize);

// // Call rotateLeftAndToggleContent when the button is clicked
// document.getElementById('changeToRec-{{ day }}').addEventListener('click', rotateLeftAndToggleContent);

var total_day = document.getElementsByClassName('tab-pane')
var isdoneJourneyVisible = {};
for( var i = 0; i < total_day.length; i++ ){
  isdoneJourneyVisible[i+1] = false;
}
function clickChangeDone(day=null) {
  if(day === null){
    day = globalDay;
  }
  console.log(day)
  const checkRec = document.getElementById('checkRec-' + day);
  const done = document.getElementById('done-' + day);
  const button = document.getElementById("changeToRec-" + day);
  isdoneJourneyVisible[day] = !isdoneJourneyVisible[day];
  if (isdoneJourneyVisible[day]) {
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
// RWD文字切圖示按鈕
const repeatBtn = document.querySelector('.changeToRec');

function changeRepeatBtnTxt() {
  if (window.innerWidth <= 690) {
    if (repeatBtn.textContent === '重新推薦') {
      // repeatBtn.classList.add('repeatIcon_btn');
      repeatBtn.innerHTML = '<i class="fa-solid fa-repeat"></i>';
    } else if (repeatBtn.textContent === '景點排序') {
      // repeatBtn.classList.add('doneIcon_btn');
      repeatBtn.innerHTML = '<i class="fa-solid fa-route"></i>';
    }
  }
  if(window.innerWidth > 690){
    if(repeatBtn.innerHTML === '<i class="fa-solid fa-repeat"></i>'){
      repeatBtn.innerHTML = '重新推薦';
    }else if(repeatBtn.innerHTML === '<i class="fa-solid fa-route"></i>'){
      repeatBtn.innerHTML = '景點排序';
    }
  }
}


// 送出功能整合到clickChangeDone函数中
// 點擊送出會切換到景點排序頁面
function submitAction(day) {

  const checkRec = document.getElementById('checkRec-' + globalDay);
  const done = document.getElementById('done-' + globalDay);
  const button = document.getElementById("changeToRec-" + globalDay);

  checkRec.style.transform = 'rotateY(180deg)';
  done.style.transform = 'rotateY(0deg)';
  button.textContent = "重新推薦";
  button.style.backgroundColor = "rgb(255, 41, 101)";
  isdoneJourneyVisible = true;

  submitRecommend();
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

var isSimilarVisible = true;
function openSimilarBtn() {

  var openSimilar = $('.openSimilar');

  if (isSimilarVisible) {
    openSimilar.animate({
      height: "show"
    }, 500);
  } else {
    openSimilar.animate({
      height: "hide"
    }, 300);
  }

  isSimilarVisible = !isSimilarVisible
}
// 當頁面載入後，呼叫一次以顯示相似元素
$(document).ready(function () {
  openSimilarBtn();
});


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
  checkbox.checked = !checkbox.checked;
  console.log(checkbox);
  var div = checkbox.parentElement.parentElement; // 取得包含checkbox的div
  if (checkbox.checked) {
    div.classList.add("pickimg");
    now_click_attractions[globalDay].add(aid);
    inputBottom();

  } else {
    div.classList.remove("pickimg");
    now_click_attractions[globalDay].delete(aid);
    inputBottom();
  }

}

// pick spot 刪除下面戰存的景點時
function pickspotBottom(aid) {
  try{
    const container = document.getElementById('ch-'+globalDay);
    const elements = container.querySelector('.imgcheck[value="' + aid + '"]');
    console.log(elements);
    pickspot(elements, aid);
  }catch(e){
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


// 底部暫存區塊
$(document).ready(function () {
  var isContentHidden = true;
  var originalHeight = $(document).height();
  var bottomHeight = $('.bottom').height();
  var contentHeight = $("#hiddenContent").height(); // 計算高度
  var upDown_icon = $('#upDown_icon');

  var originalScrollPos = 0;

  $("#controller").click(function () {
    if (isContentHidden) {
      $("#hiddenContent").slideDown(function () {
        // 展開內容並滑道也面底部
        var newHeight = originalHeight + contentHeight / 2;
        $('body').css('height', newHeight);
        window.scrollTo({
          top: newHeight,
          behavior: 'smooth'
        });
      });
      upDown_icon.toggleClass('fa-rotate-180')
    } else {
      // 計算原始高度底部位置
      var originalBottomPos = originalHeight - $(window).height();

      $("#hiddenContent").slideUp(function () {
        // 收起後恢復原網頁高度
        $('body').css('height', originalHeight);
        window.scrollTo({
          top: originalBottomPos,
          behavior: 'smooth'
        });
      });

      upDown_icon.toggleClass('fa-rotate-180')
    }
    isContentHidden = !isContentHidden;
  });
});

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
      console.log(checkbox.closest('.col-md-6'));
      checkbox.closest('.col-md-6').classList.add('pickimg');
    }
  });
}


function inputBottom(day=null){
  if(day === null){
    day = globalDay;
  }
  $.ajax({
    url:"/attractions",
    type: "GET",
    data: {
      aidlist:Array.from(now_click_attractions[day]).join(','),
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
function checkHasData(){
    const leftDev = document.querySelectorAll(".recAndDone");
    console.log(leftDev);
    leftDev.forEach(function (container, index) {
      const hasAttractions = container.querySelector('.innerlist');
      // console.log(hasAttractions);
      if (hasAttractions != null) {
        const changeToRec = container.querySelector('.changeToRec').id;
        clickChangeDone(changeToRec.charAt(changeToRec.length - 1))
      }
    });
}

function checkHasLocationData(){
  const location = document.querySelectorAll(".hiddenUserLocation");
  console.log(location);
  location.forEach(function (container, index) {
    // console.log(hasAttractions);
    if (container.value != null) {
      startRecommend(container.value,index)
    }
  });
}

//用來把有的資料放入暫存區
function checkHasDataBottom(){
  
}

checkHasDataBottom()
window.onload = changeRepeatBtnTxt;
window.addEventListener('resize', changeRepeatBtnTxt);

