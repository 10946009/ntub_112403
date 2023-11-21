function watchQuestions() {
  // 一點擊張貼則評論數＋1
  var allAskContainers = document.querySelectorAll(".all_ask_qa_con");
  console.log(allAskContainers);
  allAskContainers.forEach(function (container, index) {
    var postButton = container.getElementsByClassName("all_ask_btn_ok");
    if (postButton.length === 0) {
      return;
    }
    var commentCountElement = container.querySelector("#commentCountElement");
    for (let i = 0; i < postButton.length; i++) {
      postButton[i].addEventListener("click", function () {
        commentCountElement.textContent = parseInt(commentCountElement.textContent) + 1;
      });
    }



    // 回覆問題時，可以將結果呈現在上面
    container
      .querySelector("#all_ask_btn_ok")
      .addEventListener("click", function () {
        let currentDate = new Date(); // 不提供參數即為當前日期和時間
        let options = { month: 'short', day: 'numeric', year: 'numeric' };
        let formattedDate = currentDate.toLocaleDateString('en-US', options);

        var answerContent = container.querySelector("#answer_qa").value;
        var newComment = document.createElement("div");
        newComment.className = "comment";
        newComment.innerHTML =`
        <div class="avatar">
            <img src="${ userPhoto }" alt="User Avatar">
        </div>
        <div class="comment-content">
            <h6 class="username">
            ${ username }<br>
                <span style="color: rgb(213, 160, 37); font-size: 12px; font-style: italic;">
                    <span style="color: gray; font-size: 12px; font-style: italic;">${ formattedDate }&ensp;</span>
                </span>
            </h6>
            <h6 style="margin-bottom: 20px;"> <div>${answerContent}</div></h6>
        </div>
    `;
        var commentQa = container.querySelector("#comment_new");
        commentQa.appendChild(newComment);
        container.querySelector("#answer_qa").value = "";
        commentQa.style.display = "block";
      });

    // 初始化時檢查textarea的內容
    if (user_ask.value.trim() === "") {
      ask_btn_ok.style.color = "grey";
      ask_btn_ok.style.border = "none";
      ask_btn_ok.style.pointerEvents = "none";
    } else {
      ask_btn_ok.style.color = "black";
      ask_btn_ok.style.border = "#000 solid";
      ask_btn_ok.style.pointerEvents = "auto";
    }

    // 判斷回覆問題時，textarea有沒有東西
    var textarea = container.querySelector("#answer_qa");
    var postButton = container.querySelector("#all_ask_btn_ok");
    textarea.addEventListener("input", function () {
      if (textarea.value.trim() === "") {
        postButton.style.color = "grey";
        postButton.style.border = "none";
        postButton.style.pointerEvents = "none"; // 禁用點擊事件
      } else {
        postButton.style.color = "black";
        postButton.style.border = "#000 solid";
        postButton.style.pointerEvents = "auto"; // 啟用點擊事件
      }
    });
    // 初始化時檢查textarea的內容
    if (textarea.value.trim() === "") {
      postButton.style.color = "grey";
      postButton.style.border = "none";
      postButton.style.pointerEvents = "none";
    } else {
      postButton.style.color = "black";
      postButton.style.border = "#000 solid";
      postButton.style.pointerEvents = "auto";
    }
    // 點擊還有一個答案的功能
    var comment_qa = container.querySelector("#comment_qa");
    var qa_text = container.querySelector("#qa_text");
    if (qa_text) {
      qa_text.addEventListener("click", function () {
        qa_text.style.display = "none";
        comment_qa.style.display = "block";
      });
    }
    // 關閉查看所有圖片方塊
    var see_all_btn = container.querySelector("#see_all_btn");
    var photo_big_att_container = container.querySelector(
      "#photo_big_att_container"
    );
    var photo_att = container.querySelector("#photo_att");

    container.addEventListener("click", function (event) {
      if (event.target == photo_att) {
        photo_att.style.display = "none";
      }
    });

    // ask_tips提示點擊(查看)
    var icon1 = container.querySelector("#myIcon1");
    var tooltip2 = container.querySelector("#myTooltip2");
    var all_ask_qa_container = container.querySelector("#all_ask_qa_container");

    icon1.addEventListener("click", function () {
      if (tooltip2.style.display === "block") {
        tooltip2.style.display = "none";
      } else {
        tooltip2.style.display = "block";
      }
    });
    container.addEventListener("click", function (event) {
      if (event.target == all_ask_qa_container) {
        tooltip2.style.display = "none";
      }
    });
  });
}
