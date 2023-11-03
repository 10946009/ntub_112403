// 按鈕變文字
function clickOpen(button) {
  const isDetails = button.dataset.isDetails === 'true' || false;

  if (!isDetails) {
    button.textContent = "關閉行程";
    button.style.backgroundColor = "#F55";
    button.dataset.isDetails = 'true';
  } else {
    button.textContent = "詳細行程";
    button.style.backgroundColor = "rgb(255, 240, 126)";
    button.dataset.isDetails = 'false';
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
  $(".shareFilter_btn").each(function() {
    if ($(this).attr("href") === currentwin) {
      $(this).addClass("shareFilter_btn_click");
    }
  });
})