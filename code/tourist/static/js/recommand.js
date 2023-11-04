
function startRecommand(user_location,day){
    nowtime = document.getElementById('nowtime-' + day);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            user_location: user_location,
            nowtime: nowtime.value,
            ct_status: 0,
        },
        success: function (response) {
          console.log("推薦回傳成功" + response.m_list);
          console.log("response.crow_opening_list" + response.crow_opening_list);
        },
  
        error: function () {
            console.log('推薦回傳有錯誤!!!');
        },
      });
}