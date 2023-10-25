// $(function(){
//     $(".details{{ item.my_history.id }}btn").click(function(){
//       $("#details{{ item.my_history.id }}").slideToggle('slow',function(){
//         if($(this).is(":visible")){
//           $(".details{{ item.my_history.id }}btn").text("收起資料")
//           $(".details{{ item.my_history.id }}btn").css("background-color","rgb(255, 85, 85)")
//         }else{
//           $(".details{{ item.my_history.id }}btn").text("詳細資料")
//           $(".details{{ item.my_history.id }}btn").css("background-color","")
//         }
//       })
//     })
//   })
document.addEventListener('DOMContentLoaded', function () {

  // 获取所有的 "詳細資料" 按钮
  const detailButtons = document.querySelectorAll(".more_btn");

  // 为每个按钮添加点击事件监听
  detailButtons.forEach(button => {
    button.addEventListener("click", function () {
      const targetId = button.getAttribute("data-target");
      const targetDiv = document.getElementById(targetId);

      if (targetDiv) {
        // 获取目标 div 的当前高度
        const currentHeight = targetDiv.clientHeight;
        const targetHeight = targetDiv.scrollHeight;

        // 切换目标 div 的显示状态和动画
        if (targetDiv.classList.contains("hidden-details")) {
          targetDiv.classList.remove("hidden-details");
          animateExpand(targetDiv, currentHeight, targetHeight);

          button.textContent = "收起資料";
          button.style.textShadow = "3px 2px 3px rgb(60, 60, 60)";
          button.style.backgroundColor = "rgb(255, 85, 85)";
        } else {
          animateCollapse(targetDiv, currentHeight);
          button.textContent = "預覽行程";
          button.style.color = "";
          button.style.backgroundColor = "";
        }
      }
    });
  });
});

function animateExpand(element, startHeight, endHeight) {
  element.style.maxHeight = startHeight + "px";
  element.style.overflow = "hidden";

  requestAnimationFrame(function () {
    element.style.transition = "max-height 0.3s ease-in-out";
    element.style.maxHeight = endHeight + "px";
  });
}

function animateCollapse(element, startHeight) {
  element.style.maxHeight = startHeight + "px";

  requestAnimationFrame(function () {
    element.style.transition = "max-height 0.3s ease-in-out";
    element.style.maxHeight = "0";
    element.style.overflow = "hidden";
  });

  element.addEventListener("transitionend", function () {
    element.style.transition = "";
    element.style.maxHeight = "";
    element.classList.add("hidden-details");
  }, { once: true });
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