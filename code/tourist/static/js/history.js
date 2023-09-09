/*展開詳細行程more*/
document.addEventListener("DOMContentLoaded", function(){
  const buttons = document.querySelectorAll(".more_btn");
  const openmoreDivs = document.querySelectorAll(".openmore");

  // 設置每個按鈕的點擊事件監聽器
  buttons.forEach((button, index) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();// 阻止錨點的默認跳轉行為
        
        const targetID = button.getAttribute("data-target");
        console.log("目前點擊的id為"+targetID);
        const targetDiv = document.getElementById("more"+targetID);

        // 隱藏所有內容區域
        openmoreDivs.forEach((div) => {
            div.style.display = "none";
        });
        
        
        const isbutton = button.getAttribute("data-expanded") === "true";
        // 切换按钮的状态和文本
        buttons.forEach((btn) => {
            if (btn === button) {
                if (isbutton) {
                    btn.textContent = "詳細資料";
                    btn.style.color = "";
                    btn.style.backgroundColor = "";
                    btn.style.textShadow = "";
                    btn.setAttribute("data-expanded", "false");
                } else {
                    btn.textContent = "收起資料";
                    btn.style.color = "white";
                    btn.style.textShadow = "3px 2px 3px rgb(60, 60, 60)";
                    btn.style.backgroundColor = "rgb(255, 85, 85)";
                    btn.setAttribute("data-expanded", "true");
                }
            } else {
                btn.textContent = "詳細資料";
                btn.style.color = "";
                btn.style.backgroundColor = "";
                btn.style.textShadow = "";
                btn.setAttribute("data-expanded", "false");
            }
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
            const moreElements = document.querySelectorAll(".more");
            const idmore = [];
            moreElements.forEach((element) => {
                const id = element.id;
                idmore.push(id);
            });
            console.log(idmore);

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
            }
        });
    });

});
