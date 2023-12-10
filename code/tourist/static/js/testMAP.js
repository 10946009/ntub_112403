var locations = [
  { lat: 25.0749424, lng: 121.6206319 },
  { lat: 25.0962609, lng: 121.5164742 },
  { lat: 25.0507753, lng: 121.5597548 },
  // 添加更多经纬度...
];

var map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: locations[0]
  });

  // 初始路线
  updateMap();
}

function updateMap() {
  var startLat = parseFloat(document.getElementById('startLat').value) || locations[0].lat;
  var startLng = parseFloat(document.getElementById('startLng').value) || locations[0].lng;
  var endLat = parseFloat(document.getElementById('endLat').value) || locations[locations.length - 1].lat;
  var endLng = parseFloat(document.getElementById('endLng').value) || locations[locations.length - 1].lng;

  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  var waypoints = locations.slice(1, -1).map(function(location) {
    return { location: new google.maps.LatLng(location.lat, location.lng) };
  });

  var request = {
    origin: new google.maps.LatLng(startLat, startLng),
    destination: new google.maps.LatLng(endLat, endLng),
    waypoints: waypoints,
    travelMode: 'DRIVING'
  };

  directionsService.route(request, function(result, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(result);
      addMarkers(map, result.routes[0].legs);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}

function addMarkers(map, legs) {
  for (var i = 0; i < legs.length; i++) {
    var marker = new google.maps.Marker({
      position: legs[i].start_location,
      map: map,
    });
    marker = new google.maps.Marker({
      position: legs[i].end_location,
      map: map,
    });
  }
}