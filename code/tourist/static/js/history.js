/*展開詳細行程more*/
// 获取所有的 "詳細資料" 按钮
// const detailButtons = document.querySelectorAll(".more_btn");
// const openmore = document.getElementsByClassName(".openmore");

// // 为每个按钮添加点击事件监听
// detailButtons.forEach(button => {
//   button.addEventListener("click", function() {
//     const targetId = button.getAttribute("data-target");
//     const targetDiv = document.getElementById(targetId);
    
//     if (targetDiv) {
//       // 切换目标 div 的显示状态
//       targetDiv.classList.toggle("hidden-details");
//     }
//   });
// });

const moreButton = document.querySelector(".more_btn");
const openmore = document.querySelector(".openmore");
const tabs = document.querySelectorAll(".nav-link");
const contents = document.querySelectorAll(".content");

moreButton.addEventListener("click", function () {
  if (openmore.style.display === "none" || openmore.style.display === "") {
    openmore.style.display = "block";
  } else {
    openmore.style.display = "none";
  }
});

tabs.forEach(tab => {
  tab.addEventListener("click", function (event) {
    event.preventDefault();
    // 隐藏所有内容
    contents.forEach(content => {
      content.style.display = "none";
    });
    
    // 显示与点击标签相关的内容
    const tabId = this.getAttribute("data-tab");
    const contentToShow = document.getElementById("content" + tabId);
    if (contentToShow) {
      contentToShow.style.display = "block";
    }
  });
});