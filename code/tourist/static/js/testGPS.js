// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
// ---------------初始化Google Maps服务
var geocoder = new google.maps.Geocoder();
var mapButton = document.getElementById("mapButton");
var okButton = document.getElementById("okButton");
var userLocation = document.getElementById("userLocation");
var map_display = document.getElementById("map");
var map = null; // 地图对象
var marker = null;//地圖上的標記

//按鈕事件---------------------------------------------
okButton.addEventListener("click", function () {
  map_display.style.display = "none";
});
//地圖事件---------------------------------------------
mapButton.addEventListener("click", function () {
  map_display.style.display = "";
  // 打开地图以选择位置
  var map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 25.047, lng: 121.513 },
    zoom: 12,
  });

  const searchInput = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(searchInput);

  map.controls[google.maps.ControlPosition.TOP_LEFT].push(searchInput);
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
    // 获取地点的名称
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      const placeName = place.name;

      // 获取地点的坐标
      const placeLat = place.geometry.location.lat();
      const placeLng = place.geometry.location.lng();

      console.log("地点名称：" + placeName);
      console.log("地点坐标：" + placeLat + ", " + placeLng);

      // 在地图上显示地点
      // 清除之前的标记
      marker = tagMarker(place.geometry.location, map, marker);
      // 添加点击地图事件监听器
      google.maps.event.addListener(map, "click", function (event) {
        // 获取选定位置的经纬度坐标
        var selectedLatLng = event.latLng;
        // 標記選定位置
        marker = tagMarker(selectedLatLng, map, marker);
        // // 将经纬度坐标添加到输入框
        // userLocation.value = selectedLatLng;
        // //userLocation.value = selectedLatLng.lat() + ',' + selectedLatLng.lng();
      });
    });
  });
  map.addListener("click", (event) => {
    // 获取点击位置的经纬度
    const clickedLat = event.latLng.lat();
    const clickedLng = event.latLng.lng();

    marker = tagMarker(event.latLng, map, marker);

    // 在控制台记录点击位置的经纬度
    console.log("点击位置的经度：" + clickedLng);
    console.log("点击位置的纬度：" + clickedLat);
  });
});

//輸入經緯度就可以顯示marker，並且將經緯度存入userLocation
function tagMarker(latlng, map, marker) {
  const redIcon = {
    url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png", // 红色标记图标
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
  userLocation.value = latlng["lat"]() + "," + latlng["lng"]();
  return marker;
}
