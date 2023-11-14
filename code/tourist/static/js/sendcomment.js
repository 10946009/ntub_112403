function sendAsk(aid){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log($('#user_ask').val());
    if (confirm("確認要送出嗎?")) {
        $.ajax({
            headers: { 'X-CSRFToken': csrftoken },
            url:`/question/${aid}/`,
            type: 'POST',
            data:
            {aid:aid,
            comment:$('#user_ask').val(),
            },
            success: function (data) {
                showInfo(aid);
                alert('成功提交!');
            },
            error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}

function sendAnswer(qid){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let answer = document.querySelector(`textarea[name="answer_qa${qid}"]`).value;
    console.log(answer);
    if (confirm("確認要送出嗎?")) {
        $.ajax({
            headers: { 'X-CSRFToken': csrftoken },
            url:`/question_answer/${qid}/`,
            type: 'POST',
            data:
            {qid:qid,
            comment:answer,
            },
            success: function (data) {
                alert('成功提交!');
            },
            error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}

function sendComment(aid){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log($('#user_share_comment').val());
    if (confirm("確認要送出嗎?")) {
        $.ajax({
            headers: { 'X-CSRFToken': csrftoken },
            url:`/comment/${aid}/`,
            type: 'POST',
            data:
            {aid:aid,
            comment:$('#user_share_comment').val(),
            },
            success: function (data) {
                showInfo(aid);
                alert('成功提交!');
                
            },
            error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
    }
    
}
// 當點擊某個元素時觸發的函式，傳入的參數為觸發點擊事件的元素
function showInfo(aId) {
    var content1 = document.getElementById("replaceable-content");
    var content2 = document.getElementById("id01");
    var pointBack = document.getElementById("pointItem" + aId);
    if (aId) {
        // 發起 AJAX 請求
        $.ajax({
            url: '',  // 伺服器端的 URL
            type: 'GET',  // 請求類型為 GET
            data: {
                a_id: aId  // 傳遞給伺服器的參數，以 a_id 為名
            },
            success: function (response) {
                // 當請求成功時執行的處理程式
                const attractions_detail_div = $('#id01');
                attractions_detail_div.html(response['attractions_detail_html']);
                console.log(attractions_detail_div)
                content1.style.display = "none";
                content2.style.display = "block";
                const attractionsDetailName = document.getElementById('attractions-detail-name');
                attractionsDetailName.scrollIntoView({ behavior: 'smooth', block: 'center' }); // 使用 "smooth" 选项创建平滑的滚动效果
                // 取得模態框元素
                // var showInfo = document.getElementById("id01");
                // // 將模態框的顯示樣式設定為 "block"，顯示模態框
                // showInfo.style.display = "block";

            },
            error: function (xhr, status, error) {
                // 請求失敗時的處理
                console.log("AJAX請求失敗: " + error);
            }
        });
    } else {
        content1.style.display = "block";
        content2.style.display = "none";
        console.log(pointBack);
        pointBack.scrollIntoView({ behavior: 'smooth', block: 'center' }); // 使用 "smooth" 选项创建平滑的滚动效果
    }

}
// document.getElementById("ask-content").addEventListener("submit", function(event) {
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     event.preventDefault(); // 阻止表单的默认提交行为
//     if (confirm("確認要送出嗎?")) {
//         var formData = new FormData(this);
//         console.log(formData);
//         $.ajax({
//             headers: { 'X-CSRFToken': csrftoken },
//             url: $(this).attr('action'),
//             type: 'POST',
//             data:formData,
//             success: function (data) {
//                 alert('成功提交!');
//             },
//             error: function (xhr, errmsg, err) {
//                 alert(xhr.status + ": " + xhr.responseText);
//             }
//         });
//     }}
// );



var allComment = document.querySelectorAll(".userComment");
console.log("allComment", allComment);
allComment.forEach(function (container, index) {
    // 點讚會變讚（點回去會沒有）只有第一個大標有這個功能
    var likeButton = container.querySelector("#likeButton");
    var likeIcon = container.querySelector(".fa-thumbs-up");
    var likeCountElement = container.querySelector("#likeCount");
    
    likeButton.addEventListener("click", function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            headers: { 'X-CSRFToken': csrftoken },
            url: '/comment/like/',
            type: 'POST',
            data: {
                comment_id: container.id
            },
            success: function (response) {
                console.log(response);
            },
            error: function (xhr, status, error) {
                console.log("AJAX請求失敗: " + error);
            }});
      if (likeIcon.classList.contains("fa-regular")) {
        likeIcon.classList.remove("fa-regular");
        likeIcon.classList.add("fa-solid");
        likeCountElement.textContent = parseInt(likeCountElement.textContent) + 1;
      } else {
        likeIcon.classList.remove("fa-solid");
        likeIcon.classList.add("fa-regular");
        likeCountElement.textContent = parseInt(likeCountElement.textContent) - 1;
      }
      
    });
});