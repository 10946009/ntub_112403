/*展開詳細行程more*/
// 获取所有的 "詳細資料" 按钮
const detailButtons = document.querySelectorAll(".more_btn");

// 为每个按钮添加点击事件监听
detailButtons.forEach(button => {
  button.addEventListener("click", function() {
    const targetId = button.getAttribute("data-target");
    const targetDiv = document.getElementById(targetId);
    
    if (targetDiv) {
      // 切换目标 div 的显示状态
      targetDiv.classList.toggle("hidden-details");
    }
  });
});

// document.addEventListener("DOMContentLoaded", function() {
//   var navLinks = document.querySelectorAll(".nav-link");
//   var contents = document.querySelectorAll(".content");

//   navLinks.forEach(function(navLink) {
//     navLink.addEventListener("click", function(event) {
//       event.preventDefault();

//       var selectedTab = navLink.getAttribute("data-tab");

//       contents.forEach(function(content) {
//         content.style.display = "none";
//       });

//       var selectedContent = document.getElementById("content" + selectedTab);
//       if (selectedContent) {
//         selectedContent.style.display = "block";
//       }
//     });
//   });
// });
