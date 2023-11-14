// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
//<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"> <>
// ---------------初始化Google Maps服务
var geocoder = new google.maps.Geocoder();

var map = null; // 地图對象
var marker = null;//地圖上的標記

//按鈕事件---------------------------------------------
function clickOkButton(day){
  var map_display = document.getElementById("map-" + day);
  map_display.style.display = "none";
  const searchInput = document.getElementById("pac-input-" + day);
  searchInput.style.display = "none";
  const okButton = document.getElementById("okButton-" + day); //關閉地圖的btn
  okButton.style.display = "none";
}

//地圖事件---------------------------------------------!!!!!!!!!!!!!!!!!
function get_map(day){
  var userLocationName = document.getElementById("userLocationName-" + day);
  var userLocation = document.getElementById("userLocation-" + day);
  var map_display = document.getElementById("map-" + day);
  const okButton = document.getElementById("okButton-" + day); //關閉地圖的btn

  okButton.style.display = "";
  map_display.style.display = "";
  // 打開地圖以選擇位置
  var map = new google.maps.Map(document.getElementById("map-" + day), {
    center: { lat: 25.047, lng: 121.513 },
    zoom: 12,
  });

  const searchInput = document.getElementById("pac-input-" + day);
  searchInput.style.display = "";
  const searchBox = new google.maps.places.SearchBox(searchInput);

  // map.controls[google.maps.ControlPosition.TOP_LEFT].push(searchInput);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    // 獲取地點的名稱
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      const placeName = place.name;

      // 獲取地點的座標
      const placeLat = place.geometry.location.lat();
      const placeLng = place.geometry.location.lng();
      userLocationName.textContent = searchInput.value ;
      userLocation.value = placeLat + ',' + placeLng; // 將經緯度寫進html
      startRecommend(userLocation.value,day)
      console.log("地点名称：" + placeName);
      console.log("地点坐标：" + placeLat + ", " + placeLng);

      // 在地图上顯示地點
      // 清除之前的標記
      marker = tagMarker(place.geometry.location, map, marker);
      // 添加點擊地图事件監聽器
      google.maps.event.addListener(map, "click", function (event) {
        // 獲取選定位置的經緯度座標
        var selectedLatLng = event.latLng;
        // 標記選定位置
        marker = tagMarker(selectedLatLng, map, marker);
        // // 將經緯度座標添加到输入框
        // userLocation.value = selectedLatLng;
      });
    });
  });
  map.addListener("click", (event) => {
    var close_title = document.getElementsByClassName("gm-ui-hover-effect")[0]
    
    //如果訊息視窗已經存在就把它關掉
    if(close_title){
      close_title.click()
    }

    // 獲取點擊位置的經緯度
    const clickedLat = event.latLng.lat();
    const clickedLng = event.latLng.lng();
    
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: event.latLng }, (results, status) => {
      if (status === "OK" && results[0]) {
        const address = results[0].formatted_address;
        var title = document.getElementsByClassName("title full-width")
        
        
        searchInput.value = address  //點擊時修改searchbox的文字

        marker = tagMarker(event.latLng, map, marker); //呼叫地圖紅色標記(大頭針)

        if (title[0]){
          const placeName = title[0].textContent 

          console.log("点击位置的名字+地址：" + placeName + address);
          userLocationName.textContent = address + placeName;
          
        }else{
          console.log("点击位置的地址：" + address);
          userLocationName.textContent = address;
        }
        
      } else {
        console.error("无法获取地址信息");
      }
    });

    // 在控制台紀錄點擊位置的經緯度
    console.log("点击位置的经度：" + clickedLng);
    console.log("点击位置的纬度：" + clickedLat);
    userLocation.value = clickedLat + "," + clickedLng;// 將經緯度寫進html 
    startRecommend(userLocation.value,day)
    

  });
}


//輸入經緯度就可以顯示marker，並且將經緯度存入userLocation
function tagMarker(latlng, map, marker) {
  const redIcon = {
    url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png", // 紅色標記圖標
    size: new google.maps.Size(32, 32),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(16, 32),
  };
  // 創建新的紅色標記
  if (marker) {
    marker.setMap(null);
  }
  marker = new google.maps.Marker({
    position: latlng,
    map: map,
    icon: redIcon,
  });
  return marker;
}
