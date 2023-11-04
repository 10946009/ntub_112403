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
                alert('成功提交!');
            },
            error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
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
