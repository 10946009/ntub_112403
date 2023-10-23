//收藏
var heart = document.getElementsByClassName('heart_icon');

// var span = document.getElementsByClassName('count');
for(var i = 0;i < heart.length; i++){
    // var count;
    (function(i){
        heart[i].onclick = function(){
          var isFavorite = this.getAttribute("data-isfavorite");
          if(isFavorite==="0"){
            this.setAttribute("data-isfavorite", "1");//無收藏被點擊
            this.className = "fa-solid fa-heart heart_icon active_heart";
            id = this.getAttribute("data-id");
            type = this.getAttribute("data-type");
            addFavorite_index(id,type);
            // ++span[i].innerHTML;
          }else{
            ans = window.confirm('您確定要移除此景點嗎?');

            if (ans == true) {

              console.log("成功");
              this.setAttribute("data-isfavorite", "0");//點擊取消收藏
              this.className = "fa-solid fa-heart heart_icon";
              id = this.getAttribute("data-id");
              type = this.getAttribute("data-type");
              addFavorite_index(id,type);

            }else {

              console.log("取消");

            }
          }
          
        }  
    })(i);
} 

// 移除收藏
function toggleFavorite(heartIcon, a_id) {
  /*if (heartIcon.style.color === "red") {
    heartIcon.style.color = "gray";
  } else {
    heartIcon.style.color = "red";
  }*/
  var csrftoken = "{{ csrf_token }}";
  ans = window.confirm('您確定要移除此景點嗎?');
  if (ans == true) {
    console.log("成功");
    window.location.href = `/del_favorite/${a_id}`;
  } else {
    console.log("取消");
  }

}
function delTravelFavorite(heartIcon, ct_id) {
  /*if (heartIcon.style.color === "red") {
    heartIcon.style.color = "gray";
  } else {
    heartIcon.style.color = "red";
  }*/
  var csrftoken = "{{ csrf_token }}";
  ans = window.confirm('您確定要移除此行程嗎?');
  if (ans == true) {
    console.log("成功");
    window.location.href = `/del_travel_favorite/${ct_id}`;
  } else {
    console.log("取消");
  }

}

// document.addEventListener('DOMContentLoaded', function () {
//   const locationHearts = document.querySelectorAll('.location-heart');

//   locationHearts.forEach(function (heart) {
//     heart.addEventListener('click', function () {
//       this.classList.toggle('active');
//     });
//   });
// });

// function toggleFavorite(heartIcon) {
//   if (heartIcon.style.color === "red") {
//     heartIcon.style.color = "gray";
//   } else {
//     heartIcon.style.color = "red";
//   }
// }
// function toggleFavorite(element) {

//   element.classList.toggle("zoomIn");
// }
//CC改的
document.addEventListener('DOMContentLoaded', function () {
  const selectedTab = localStorage.getItem('selectedTab');
  if (selectedTab === 'contact') {
    document.getElementById('home-tab').classList.remove('active');
    document.getElementById('home').classList.remove('show', 'active');

    document.getElementById('contact-tab').classList.add('active');
    document.getElementById('contact').classList.add('show', 'active');
  }
});



//原本的
// function saveTabState(tabName) {
//   localStorage.setItem('selectedTab', tabName);
// }
// document.addEventListener('DOMContentLoaded', function() {
//   const selectedTab = localStorage.getItem('selectedTab');
//   if (selectedTab === 'contact') {
//     document.getElementById('contact-tab').click();
//   }
// });
