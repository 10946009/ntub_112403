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
        const attractions_detail_div = $('#AttractionsContainer-'+ globalDay );
        attractions_detail_div.html(response['recommend_attractions_list']);
        checkAndAddClass();
      },

      error: function () {
          console.log('推薦回傳有錯誤!!!');
      },
    });
}

function similarRecommend(){
  aid_list = Array.from(now_click_attractions[globalDay]);
  nowtime = document.getElementById('nowtime-' + globalDay);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const similar_attractions_detail_div = $('#SimilarRecommend');
  $.ajax({
      type: "POST",
      headers: { 'X-CSRFToken': csrftoken },
      data: {
          aid_list: aid_list,
          nowtime: nowtime.value,
          ct_status: 1,
      },
      beforeSend: function () {
        console.log("请求发送中...");
        similar_attractions_detail_div.html("<div>正在為您推薦相似景點…</div>");
    },
      success: function (response) {
        console.log( response);
        similar_attractions_detail_div.html(response['recommend_attractions_list']);
        checkAndAddClass();
      },

      error: function () {
          console.log('推薦相似回傳有錯誤!!!');
      },
    });

}

function submitRecommend(){
  nowtime = document.getElementById('nowtime-' + globalDay);
  const total_aid_list = Array.from(now_click_attractions[globalDay]);

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const order_attractions_detail_div = $('#orderAttractions-'+ globalDay );
  $.ajax({
      type: "POST",
      headers: { 'X-CSRFToken': csrftoken },
      data: {
          total_aid_list: total_aid_list,
          nowtime: nowtime.value,
          ct_status: 2,
      },
      beforeSend: function () {
        console.log("请求发送中...");
        order_attractions_detail_div.html("<div>正在排序中...</div>");
    },
      success: function (response) {
        console.log(response);
        order_attractions_detail_div.html(response['order_attractions']);
        checkAndAddClass();
      },

      error: function () {
          console.log('送出推薦回傳有錯誤!!!');
      },
    });

}