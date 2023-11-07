//我是儲存~~~
function createSave() {
  var nowtime = document.getElementById("nowtime-" + globalDay);
  var userLocation = document.getElementById("userLocation-" + globalDay);
  var orderAttractions = document.getElementById(
    "orderAttractions-" + globalDay
  );
  var spotElements =
    orderAttractions.getElementsByClassName("innerlist");
  let all_id = [];
  console.log(spotElements);
  for (var i = 0; i < spotElements.length; i++) {
    var spotElement = spotElements[i];
    // 使用dataset属性获取自定义数据
    var id = spotElement.dataset.id;
    var stay = spotElement.dataset.stay;
    // 输出自定义数据
    console.log("ID: " + id);
    console.log("停留时间: " + stay);
    all_id.push(id);
  }
  // if (all_id) {
  //   all_id = all_id.textContent;
  // } else {
  //   all_id = "";
  // }
  alert(all_id);
  console.log(nowtime, userLocation, all_id);

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
    headers: { 'X-CSRFToken': csrftoken },
    type: "POST",
    data: {
      day: globalDay,
      location: userLocation.value,
      nowtime: nowtime.value,
      all_id: all_id.join(','),
      ct_status: 3,
    },
    success: function (response) {
      // 在這裡處理伺服器回傳的 JSON 數據
      console.log(response); // 查看回傳的值
      alert("儲存成功");
    },

    error: function () {
      alert("有錯誤!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
    },
  });
}
