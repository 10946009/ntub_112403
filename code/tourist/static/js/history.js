// // 按鈕變文字
// function clickOpen(button) {
//   const isDetails = button.dataset.isDetails === 'true' || false;

//   if (!isDetails) {
//     button.textContent = "關閉行程";
//     button.style.backgroundColor = "#F55";
//     button.dataset.isDetails = 'true';
//   } else {
//     button.textContent = "詳細行程";
//     button.style.backgroundColor = "rgb(255, 240, 126)";
//     button.dataset.isDetails = 'false';
//   }
// }


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