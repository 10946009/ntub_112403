// document.getElementById("trash-icon").addEventListener("click", function() {
//   this.classList.toggle("clicked");
// });


//收藏
var heart = document.getElementsByClassName('heart_icon');

// var span = document.getElementsByClassName('count');
for (var i = 0; i < heart.length; i++) {
  // var count;
  (function (i) {
    heart[i].onclick = function () {
      var isFavorite = this.getAttribute("data-isfavorite");
      if (isFavorite === "0") {
        this.setAttribute("data-isfavorite", "1");//無收藏被點擊
        this.className = "fa-solid fa-heart heart_icon active_heart";
        // ++span[i].innerHTML;
      } else {
        this.setAttribute("data-isfavorite", "0");//點擊取消收藏
        this.className = "fa-solid fa-heart heart_icon";
        // --span[i].innerHTML;
      }
      id = this.getAttribute("data-id")
      type = this.getAttribute("data-type")
      addFavorite_index(id, type);
    }
  })(i);
}