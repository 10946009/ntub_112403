document.addEventListener('DOMContentLoaded',function(){
    
  // 获取所有的 "詳細資料" 按钮
  const detailButtons = document.querySelectorAll(".more_btn");

  // 为每个按钮添加点击事件监听
  detailButtons.forEach(button => {
    button.addEventListener("click", function () {
      const targetId = button.getAttribute("data-target");
      const targetDiv = document.getElementById(targetId);

      if (targetDiv) {
        // 切换目标 div 的显示状态
        targetDiv.classList.toggle("hidden-details");
        if (targetDiv.classList.contains("hidden-details")) {
          button.textContent = "詳細資料";
          button.style.color = ""
          button.style.backgroundColor = "";
        } else {
          button.textContent = "收起資料";
          button.style.textShadow = "3px 2px 3px rgb(60, 60, 60)";
          button.style.backgroundColor = "rgb(255, 85, 85)";
        }
      }
    });
  });
})