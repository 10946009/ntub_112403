function startRecommend(user_location,day){
  console.log(user_location);
  nowtime = document.getElementById('nowtime-' + globalDay);
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
        const attractions_detail_div = $('#AttractionsContainer-'+ globalDay );
        attractions_detail_div.html(response['recommend_attractions_list']);
      },

      error: function () {
          console.log('推薦回傳有錯誤!!!');
      },
    });
}

function similarRecommend(aid_list){

  // const dataSetValue = button.dataset.set;
  console.log(globalDay)
  console.log(aid_list);
  
  aid_list = Array.from(aid_list[globalDay]);
  nowtime = document.getElementById('nowtime-' + globalDay);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
      type: "POST",
      headers: { 'X-CSRFToken': csrftoken },
      data: {
          aid_list: aid_list,
          nowtime: nowtime.value,
          ct_status: 1,
      },
      success: function (response) {
        console.log( response);
        const similar_attractions_detail_div = $('#SimilarRecommend-'+ globalDay );
        similar_attractions_detail_div.html(response['recommend_attractions_list']);
      },

      error: function () {
          console.log('推薦相似回傳有錯誤!!!');
      },
    });

}