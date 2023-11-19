
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

function clickShow(button,ctid) {
  console.log(ctid);
  const targetDivId = button.getAttribute('data-target');
  const targetDiv = document.getElementById(targetDivId);
  const changeHistory = document.getElementById('changeHistory');
  if (targetDiv.style.display === 'block') {
    targetDiv.style.display = 'none';
    button.textContent = '詳細行程';
    button.style.backgroundColor = "rgb(255, 240, 126)";
  } else {
    // 隱藏所有類似的詳細資訊 div
    document.querySelectorAll(".openDetailDiv").forEach(div => {
      div.style.display = 'none';
    });
    // 顯示目標詳細資訊 div
    targetDiv.style.display = 'block';
    button.textContent = '關閉閱覽';
    button.style.backgroundColor = "#F55";
    $.ajax({
      type: "GET",
      url: "/history/info/",
      data: {
        'id': ctid,
      },
      success: function (data) {
        changeHistory.innerHTML = data;
      },
      error: function (xhr, textStatus, errorThrown) {
        console.error("Error:", textStatus, errorThrown);
      }
    });

    
  }

  // 更改其他按鈕的文字狀態
  const allButtons = document.querySelectorAll("[class^='more_btn']");
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
const addCTXT = document.getElementById('addCTXT');

let isaddCommentSpaceVisible = false;
let isEdit = false;

function addComment() {
  console.log(1);
  addCTXT.value = '';
  if (addCommentBtn.textContent === '新增評論') {
    addCommentSpace.style.display = 'block';
    addCommentBtn.textContent = '取消評論';
  } else if(addCommentBtn.textContent === '取消評論') {
    addCommentSpace.style.display = 'none';
    addCommentBtn.textContent = '新增評論';
  }
  isaddCommentSpaceVisible = !isaddCommentSpaceVisible;
}

// 發送評論
function submitComment() {
  var commentText = document.getElementById('addCTXT').value;
  addCommentBtn.style.display = 'none';
  addCommentBtn.textContent = '新增評論';

  var newCreateComment = createCommentElement(commentText);
  insertComment(newCreateComment);

  console.log('2');
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

    var iconDiv = document.createElement('div');
    iconDiv.className = 'c_editDiv';
    iconDiv.classList.add('c_editDiv');

    // 新增編輯按鈕
    var editBtnDiv = document.createElement('div');
    editBtnDiv.className = 'c_edit_iconDiv';
    var editBtn = document.createElement('button');
    editBtn.className = 'fa-solid fa-pen-to-square c_edit_icon c_icon';
    editBtn.onclick = function () {
      editComment(textSpan);
      // iconDiv.style.display = 'none';
    };
    editBtnDiv.appendChild(editBtn);
    iconDiv.appendChild(editBtnDiv);

    // 新增刪除按鈕
    var deleteBtnDiv = document.createElement('div');
    deleteBtnDiv.className = 'c_delete_iconDiv';
    var deleteBtn = document.createElement('button');
    deleteBtn.className = 'fa-solid fa-trash c_delete_icon c_icon';
    deleteBtn.onclick = function () {
      if (confirm('確定要刪除該留言嗎？')) {
        newComment.parentNode.removeChild(newComment);
        addCommentBtn.style.display = 'block';
        console.log(6);
      }
    };
    deleteBtnDiv.appendChild(deleteBtn);
    iconDiv.appendChild(deleteBtnDiv);

    textDiv.appendChild(iconDiv);

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
    document.getElementById('addCommentSpace').style.display = 'none';
  }

}
// 編輯按鈕
function editComment(commentSpan) {
  var originalText = commentSpan.innerText;

  commentSpan.style.display = 'none';

  var editTextArea = document.createElement('textarea');
  editTextArea.value = originalText;
  editTextArea.style.width = '100%';
  editTextArea.style.height = '200px';

  var buttonsContainer = document.createElement('div'); // 創建容器元素
  buttonsContainer.style.display = 'flex'; // 使用 Flex 排列元素
  buttonsContainer.style.flexDirection = 'column'; // 垂直排列元素

  var saveEditBtn = document.createElement('button');
  saveEditBtn.textContent = '儲存';
  saveEditBtn.classList.add('saveBtn');
  saveEditBtn.onclick = function () {
    commentSpan.innerText = editTextArea.value;
    commentSpan.parentNode.removeChild(editTextArea);
    commentSpan.parentNode.removeChild(buttonsContainer); 
    commentSpan.style.display = 'block';
    editBtn.style.display = 'block';
    deleteBtn.style.display = 'block';
  };

  var cancelEditBtn = document.createElement('button');
  cancelEditBtn.textContent = '取消';
  cancelEditBtn.classList.add('cancelBtn');
  cancelEditBtn.onclick = function () {
    commentSpan.innerText = originalText;
    commentSpan.style.display = 'block';
    commentSpan.parentNode.removeChild(editTextArea);
    commentSpan.parentNode.removeChild(buttonsContainer); 
    editBtn.style.display = 'inline-block';
    deleteBtn.style.display = 'inline-block';
  };

  buttonsContainer.appendChild(saveEditBtn);
  buttonsContainer.appendChild(cancelEditBtn); 

  commentSpan.parentNode.insertBefore(editTextArea, commentSpan);
  commentSpan.parentNode.appendChild(buttonsContainer); // 將容器插入 DOM 中

  var deleteBtn = commentSpan.parentNode.querySelector('.c_delete_icon');
  deleteBtn.style.display = 'none';
  var editBtn = commentSpan.parentNode.querySelector('.c_edit_icon');
  editBtn.style.display = 'none';
}



// function editComment(){
//   console.log(3);
//   var submitedComment = document.getElementById('otherCommentTxt');
//   var editSubmitedComment = submitedComment.innerText;

//   var editTextarea = document.createElement('textarea');
//   editTextarea.value = editSubmitedComment;

//   var submitButton = document.createElement('button');
//   submitButton.innerText = '提交';
//   submitButton.onclick = function() {
//       var updatedText = editTextarea.value;
//       var newSpan = document.createElement('span');
//       newSpan.innerText = updatedText;

//       editTextarea.parentNode.replaceChild(newSpan, editTextarea);
//   };
//   // 替換原本的 span 和添加提交按鈕
//   submitedComment.parentNode.replaceChild(editTextarea, submitedComment);
//   editTextarea.parentNode.appendChild(submitButton);
// }


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



function deleteTravel(id) {
  const deleteCheck = confirm("確定要刪除嗎?");
  if (deleteCheck == false) {
    return;
  }else{
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
      headers: { 'X-CSRFToken': csrftoken },
      url: "/history/delete/",
      type: "get",
      data: {
        'id': id,
      },
      success: function (data) {
        location.reload();
      }
    });
  }
}