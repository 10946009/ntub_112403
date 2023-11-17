
// 公開or不公開
function add_favorite_share(ctid) {
  // var sharediv = document.getElementById("ct_share");
  var favoriteButton = document.getElementById("submitfavorite_share" + ctid);
  var text = document.getElementById("icontxt" + ctid);
  var isFavoriteValue = favoriteButton.getAttribute("data-isfavorite");
  if (isFavoriteValue === "1") {
    //favoriteButton.setAttribute("class", "fa-regular fa-heart");  //將來修改icon放這
    favoriteButton.setAttribute("data-isfavorite", "0");
    text.textContent = "公開";
    favoriteButton.style.color = 'black';
  } else {
    //favoriteButton.setAttribute("class", "fa-regular fa-heart");  //將來修改icon放這
    favoriteButton.setAttribute("data-isfavorite", "1");
    favoriteButton.style.color = 'orange';
    text.textContent = "已公開";
  }
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
    headers: { 'X-CSRFToken': csrftoken },
    type: "POST",
    url: "/add_favorite_share/",
    data: {
      'ctid': ctid,
    },
    success: function (data) {
      console.log(data);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.error("Error:", textStatus, errorThrown);
    }
  });
};

function clickShow(button) {
  const targetBtn = button.getAttribute('data-target');
  const showDiv = document.getElementById(targetBtn);

  if (showDiv.style.display === 'block') {
    showDiv.style.display = 'none';
    button.textContent = '詳細行程';
    button.style.backgroundColor = "rgb(255, 240, 126)";
  } else {
    document.querySelectorAll("[id^='show']").forEach(div => {
      div.style.display = "none";
    })
    showDiv.style.display = 'block';
    button.textContent = '關閉閱覽';
    button.style.backgroundColor = "#F55";
  }
  // 获取所有左侧按钮并更改非当前点击按钮的文本为 "点我出现"
  const allButtons = document.querySelectorAll("[id^='clickme']");
  allButtons.forEach(btn => {
    if (btn !== button) {
      btn.textContent = '詳細行程';
      btn.style.backgroundColor = "rgb(255, 240, 126)";
    }
  });
}

// 點新增評論按鈕
const addCommentBtn = document.getElementById('addCommentBtn');
const addCommentSpace = document.getElementById('addCommentSpace');

let isaddCommentSpaceVisible = false;
let isEdit = false;

function addComment() {
  if (!isaddCommentSpaceVisible) {
    addCommentSpace.style.display = 'block';
    addCommentBtn.textContent = '取消評論';
  } else {
    addCommentSpace.style.display = 'none';
    addCommentBtn.textContent = '新增評論';

  }
  isaddCommentSpaceVisible = !isaddCommentSpaceVisible;
}


// Change editedComment function to only handle edit initiation
function editedComment() {
  var commentTxt = document.querySelector('.row.editing .otherCommentTxt').innerText;
  var editedComment = document.querySelector('.row.editing');

  document.getElementById('addCTXT').value = commentTxt;
  addCommentSpace.style.display = 'block';
  addCommentBtn.textContent = '取消評論';

  editedComment.classList.add('editing');
  isEdit = true;
}

// 發送評論
function submitComment() {
  var commentText = document.getElementById('addCTXT').value;
  addCommentBtn.style.display = 'none';

  var newCreateComment = createCommentElement(commentText);
  insertComment(newCreateComment);
  var editedComment = document.querySelector('.row.editing');
  editedComment.querySelector('.otherCommentTxt').innerText = commentText;

  // 創建新評論
  function createCommentElement(commentText) {
    var newComment = document.createElement('div');
    newComment.className = 'row';

    var avatarDiv = document.createElement('div');
    avatarDiv.className = 'col-auto otherCommentAvatar';
    avatarDiv.innerHTML = '<img src="../static/images/cloud1.png" class="img-responsive" style="width: 100%;" alt=""><br>';
    newComment.appendChild(avatarDiv);

    var textDiv = document.createElement('div');
    textDiv.className = 'col otherCommentTxtDiv';
    var textSpan = document.createElement('span');
    textSpan.className = 'otherCommentTxt';
    textSpan.innerText = commentText;
    textDiv.appendChild(textSpan);
    newComment.appendChild(textDiv);

    return newComment;
  }

  //新增評論排序在最前面 
  function insertComment(newComment) {
    var commentSection = document.getElementById('alreadyComment');

    // Check if there are already comments
    var existingComments = commentSection.getElementsByClassName('row');

    if (existingComments.length > 0) {
      commentSection.insertBefore(newComment, existingComments[0]);
    } else {
      commentSection.appendChild(newComment);
    }
    isEdit = false;
    document.getElementById('addCommentSpace').style.display = 'none';
    document.getElementById('addCommentBtn').textContent = '編輯評論'
  }

}


$(document).ready(function () {
  var currentwin = window.location.pathname;

  // 给每个链接添加点击事件处理程序
  $(".shareFilter_btn").click(function (e) {
    $(".shareFilter_btn").removeClass("shareFilter_btn_click");
    $(this).addClass("shareFilter_btn_click");
  });

  // 设置初始选中链接的样式
  $(".shareFilter_btn").each(function () {
    if ($(this).attr("href") === currentwin) {
      $(this).addClass("shareFilter_btn_click");
    }
  });
})

// 顯示目前市第幾張圖(好像沒辦法放在圖片的右下角)
document.addEventListener("DOMContentLoaded", function () {
  var carousel = document.getElementById('carouselExampleRide');
  var counter = document.getElementById('imgCounter');
  var totalItems = carousel.querySelectorAll('.carousel-item').length; // 定義 totalItems 變數，表示總共有幾張圖片

  var carouselInstance = new bootstrap.Carousel(carousel, {
    interval: 3000
  });

  carouselInstance.update = function () {
    var activeIndex = Array.from(carousel.querySelectorAll('.carousel-item')).indexOf(carousel.querySelector('.carousel-item.active')) + 1;
    counter.innerHTML = activeIndex + '  /  ' + totalItems;
  };

  carousel.addEventListener('slid.bs.carousel', function () {
    carouselInstance.update();
  });

  carouselInstance.update();
});
