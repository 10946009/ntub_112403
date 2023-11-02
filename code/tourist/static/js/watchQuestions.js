
function watchQuestions() {
// 一點擊張貼則評論數＋1
    var postButton = document.getElementById("all_ask_btn_ok");
    var commentCountElement = document.getElementById("commentCountElement");
    var commentCount = 3;

    postButton.addEventListener("click", function () {
        commentCount++;
        commentCountElement.textContent = commentCount;
    });

    // 點讚會變讚（點回去會沒有）只有第一個大標有這個功能
    var likeButton = document.getElementById("likeButton");
    var likeIcon = document.querySelector(".fa-regular.fa-thumbs-up");
    var likeCountElement = document.getElementById("likeCount");
    var likeCount = 8;
    likeButton.addEventListener("click", function () {
        if (likeIcon.classList.contains("fa-regular")) {
            likeIcon.classList.remove("fa-regular");
            likeIcon.classList.add("fa-solid");
            likeCount++;
        } else {
            likeIcon.classList.remove("fa-solid");
            likeIcon.classList.add("fa-regular");
            likeCount--;
        }
        likeCountElement.textContent = likeCount;
    });

    // 回覆問題時，可以將結果呈現在上面
    document.getElementById("all_ask_btn_ok").addEventListener("click", function () {
        var answerContent = document.getElementById("answer_qa").value;
        var newComment = document.createElement("div");
        newComment.className = "comment";
        newComment.innerHTML = `
        <div class="avatar">
            <img src="../static/images/peka.webp" alt="User Avatar">
        </div>
        <div class="comment-content">
            <h6 class="username">
                皮卡丘<br>
                <span style="color: rgb(213, 160, 37); font-size: 12px; font-style: italic;">
                    <i class="fa-solid fa-crown"></i>在地嚮導&ensp;<br>
                    <span style="color: gray; font-size: 12px; font-style: italic;">10天前&ensp;</span>
                </span>
            </h6>
            <h6 style="margin-bottom: 20px;"> <div>${answerContent}</div></h6>
            <span style="margin-right: 20px;cursor: pointer;font-size: 18px;">
                <i class="fa-regular fa-thumbs-up" style=" color: rgb(0, 102, 255);"></i>0</span>
        </div>
    `;
        var commentQa = document.getElementById("comment_new");
        commentQa.appendChild(newComment);
        document.getElementById("answer_qa").value = "";
        commentQa.style.display = "block";
    });

    // 判斷提出問題時，textarea有沒有東西
    var user_ask = document.getElementById('user_ask');
    var ask_btn_ok = document.getElementById('ask_btn_ok');
    user_ask.addEventListener('input', function () {
        if (user_ask.value.trim() === '') {
            ask_btn_ok.style.color = 'grey';
            ask_btn_ok.style.border = 'none';
            ask_btn_ok.style.pointerEvents = 'none'; // 禁用點擊事件
        } else {
            ask_btn_ok.style.color = 'black';
            ask_btn_ok.style.border = '#000 solid';
            ask_btn_ok.style.pointerEvents = 'auto'; // 啟用點擊事件
        }
    });
    // 初始化時檢查textarea的內容
    if (user_ask.value.trim() === '') {
        ask_btn_ok.style.color = 'grey';
        ask_btn_ok.style.border = 'none';
        ask_btn_ok.style.pointerEvents = 'none';
    } else {
        ask_btn_ok.style.color = 'black';
        ask_btn_ok.style.border = '#000 solid';
        ask_btn_ok.style.pointerEvents = 'auto';
    }

    // 判斷回覆問題時，textarea有沒有東西
    var textarea = document.getElementById('answer_qa');
    var postButton = document.getElementById('all_ask_btn_ok');
    textarea.addEventListener('input', function () {
        if (textarea.value.trim() === '') {
            postButton.style.color = 'grey';
            postButton.style.border = 'none';
            postButton.style.pointerEvents = 'none'; // 禁用點擊事件
        } else {
            postButton.style.color = 'black';
            postButton.style.border = '#000 solid';
            postButton.style.pointerEvents = 'auto'; // 啟用點擊事件
        }
    });
    // 初始化時檢查textarea的內容
    if (textarea.value.trim() === '') {
        postButton.style.color = 'grey';
        postButton.style.border = 'none';
        postButton.style.pointerEvents = 'none';
    } else {
        postButton.style.color = 'black';
        postButton.style.border = '#000 solid';
        postButton.style.pointerEvents = 'auto';
    }
    // 點擊還有一個答案的功能
    var comment_qa = document.getElementById("comment_qa");
    var qa_text = document.getElementById("qa_text");
    qa_text.addEventListener("click", function () {
        qa_text.style.display = "none";
        comment_qa.style.display = "block";
    });
    
    // 關閉查看所有圖片方塊
    var see_all_btn = document.getElementById('see_all_btn');
    var photo_big_att_container = document.getElementById('photo_big_att_container');
    var photo_att = document.getElementById('photo_att');

    document.addEventListener("click", function (event) {
        if (event.target == photo_att) {
            photo_att.style.display = "none";
        }
    });
    var closePhoto = document.getElementById('closePhoto');
    closePhoto.addEventListener("click", function () {
        photo_att.style.display = "none";
    });

    // ask_tips提示點擊(查看)
    var icon1 = document.getElementById("myIcon1");
    var tooltip2 = document.getElementById("myTooltip2");
    var all_ask_qa_container = document.getElementById("all_ask_qa_container");

    icon1.addEventListener("click", function () {
        if (tooltip2.style.display === "block") {
            tooltip2.style.display = "none";
        } else {
            tooltip2.style.display = "block";
        }
    });
    document.addEventListener("click", function (event) {
        if (event.target == all_ask_qa_container) {
            tooltip2.style.display = "none";
        }
    });

}