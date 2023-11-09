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
    if (addCommentBtn.textContent === '編輯評論') {
      editedComment();
    } else {
      addCommentBtn.textContent = '取消評論';
    }
  } else {
    if (addCommentBtn.textContent === '編輯評論') {
      addCommentBtn.textContent = '取消評論';
      editedComment();
    } else {
      addCommentSpace.style.display = 'none';
      addCommentBtn.textContent = '新增評論';
    }
  }
  isaddCommentSpaceVisible = !isaddCommentSpaceVisible;
}
// Move the event listener outside of editedComment function
document.getElementById('commentSubmit').addEventListener('click', function () {
  if (isEdit) {
    var commentText = document.getElementById('addCTXT').value;
    var editedComment = document.querySelector('.row.editing');

    editedComment.querySelector('.otherCommentTxt').innerText = commentText;

    addCommentSpace.style.display = 'none';
    addCommentBtn.textContent = '編輯評論';
    isEdit = false;
  }
});

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

  if (!isEdit) {
    // Create a new comment when not in edit mode
    var newCreateComment = createCommentElement(commentText);
    insertComment(newCreateComment);
    addCommentSpace.style.display = 'none';
    addCommentBtn.textContent = '編輯評論';
  } else {
    // Logic for editing an existing comment
    var editedComment = document.querySelector('.row.editing');
    editedComment.querySelector('.otherCommentTxt').innerText = commentText;
    editedComment.classList.remove('editing');
    addCommentSpace.style.display = 'none';
    addCommentBtn.textContent = '編輯評論';
    isEdit = false;
  }
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
  // // 編輯評論
  // function editedComment() {
  //   var commentTxt = document.querySelector('.row.editing .otherCommentTxt').innerText;
  //   var editedComment = document.querySelector('.row.editing');

  //   document.getElementById('addCTXT').value = commentTxt;
  //   addCommentSpace.style.display = 'block';
  //   addCommentBtn.textContent = '取消評論';

  //   editedComment.classList.add('editing');
  //   isEdit = true;

  //   // 下面是你的提交评论的逻辑示例，应该在确认编辑后执行。
  //   document.getElementById('commentSubmit').addEventListener('click', function () {
  //     var commentText = document.getElementById('addCTXT').value;

  //     // Update the existing comment with the edited text
  //     editedComment.querySelector('.otherCommentTxt').innerText = commentText;

  //     addCommentSpace.style.display = 'none';
  //     addCommentBtn.textContent = '編輯評論';
  //     isEdit = false;
  //   });
  // }

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