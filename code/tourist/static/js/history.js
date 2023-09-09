/*展開詳細行程more*/
document.addEventListener("DOMContentLoaded", function(){
  const buttons = document.querySelectorAll(".more_btn");
  const openmoreDivs = document.querySelectorAll(".openmore");

  // 設置每個按鈕的點擊事件監聽器
  buttons.forEach((button, index) => {
      button.addEventListener("click", (event) => {
          event.preventDefault();// 阻止錨點的默認跳轉行為

          // 找到按鈕對應的 data-target 屬性的值
          const targetID = button.getAttribute("data-target");
          console.log(targetID);
          // 找到對應的內容區域
          const targetDiv = document.getElementById("more"+targetID);

          // 隱藏所有內容區域
          openmoreDivs.forEach((div) => {
              div.style.display = "none";
          });

          // 顯示點擊按鈕對應的內容區域
          if (targetDiv) {
            const istargetDiv = getComputedStyle(targetDiv).display === 'block';//getComputedStyle方法检查targetDiv的当前显示状态
            if(istargetDiv){
                targetDiv.style.display = "none";
            }else{
                targetDiv.style.display = "block";
                const firsttabDiv = document.querySelector(`[data-tab="${targetID}-1"]`);
                firsttabDiv.click();
            }
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
            event.preventDefault();

            const tabID = link.getAttribute("data-tab");
            const content = document.getElementById("content"+tabID);
            
            const idmore = ["more2","more3"];

            if (content) {
                idmore.forEach((id) => {
                    const element = document.getElementById(id);

                    if(element){
                        const allcontent = element.querySelectorAll(".content");
                        allcontent.forEach((c) => {
                            c.style.display = "none";
                        });
                        content.style.display = "block";
                    }
                })
            //     // 隱藏所有內容區域
            //     const allContent = document.getElementById("more3").querySelectorAll(".content");
            //     allContent.forEach((c) => {
            //         c.style.display = "none";
            //     });
            //     content.style.display = "block";
            }
        });
    });

});
