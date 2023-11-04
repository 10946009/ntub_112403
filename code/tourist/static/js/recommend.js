
function startRecommend(user_location,day){
  console.log(user_location);
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
          console.log( response);
          const attractions_detail_div = $('#AttractionsContainer');
          attractions_detail_div.html(response['recommend_attractions_list']);
        },
  
        error: function () {
            console.log('推薦回傳有錯誤!!!');
        },
      });
}