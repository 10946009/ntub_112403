/*展開詳細行程more*/

document.addEventListener("DOMContentLoaded", function(){
  
  
  // 選擇所有的按鈕和對應的內容區域
  const buttons = document.querySelectorAll(".more_btn");
  const openmoreDivs = document.querySelectorAll(".openmore");

  // 設置每個按鈕的點擊事件監聽器
  buttons.forEach((button, index) => {
      button.addEventListener("click", (event) => {
          // 阻止錨點的默認跳轉行為
          event.preventDefault();

          // 找到按鈕對應的 data-target 屬性的值
          const targetID = button.getAttribute("data-target");

          // 找到對應的內容區域
          const targetDiv = document.getElementById(targetID);

          // 隱藏所有內容區域
          openmoreDivs.forEach((div) => {
              div.style.display = "none";
          });

          // 顯示點擊按鈕對應的內容區域
          if (targetDiv) {
              targetDiv.style.display = "block";
          }

          // 將按鈕移到其下方的內容區域
          const parentDiv = button.closest(".mytravel");
          if (parentDiv) {
              parentDiv.parentNode.insertBefore(targetDiv, parentDiv.nextSibling);
          }
      });
  });

// 選擇所有的內容區域中的連結
const tabLinks = document.querySelectorAll(".nav-link");

// 設置每個連結的點擊事件監聽器
tabLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
      // 阻止錨點的默認跳轉行為
      event.preventDefault();

      // 找到連結對應的 data-tab 屬性的值
      const tabID = link.getAttribute("data-tab");

      // 找到對應的內容區域
      const content = document.getElementById(tabID);

      if (content) {
          // 隱藏所有內容區域
          const allContent = content.closest("#more3").querySelectorAll(".content");
          allContent.forEach((c) => {
              c.style.display = "none";
          });

          // 顯示點擊連結對應的內容
          content.style.display = "block";
      }
  });
});

});



// const moreButton = document.querySelector(".more_btn");
// const openmore = document.querySelector(".openmore");
// const tabs = document.querySelectorAll(".nav-link");
// const contents = document.querySelectorAll(".content");

// moreButton.addEventListener("click", function () {
//   if (openmore.style.display === "none" || openmore.style.display === "") {
//     openmore.style.display = "block";
//   } else {
//     openmore.style.display = "none";
//   }
// });

// tabs.forEach(tab => {
//   tab.addEventListener("click", function (event) {
//     event.preventDefault();
//     // 隐藏所有内容
//     contents.forEach(content => {
//       content.style.display = "none";
//     });
    
//     // 显示与点击标签相关的内容
//     const tabId = this.getAttribute("data-tab");
//     const contentToShow = document.getElementById("content" + tabId);
//     if (contentToShow) {
//       contentToShow.style.display = "block";
//     }
//   });
// });