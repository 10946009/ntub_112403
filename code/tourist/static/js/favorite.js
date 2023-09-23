document.addEventListener('DOMContentLoaded', function () {
  const locationHearts = document.querySelectorAll('.location-heart');

  locationHearts.forEach(function (heart) {
    heart.addEventListener('click', function () {
      this.classList.toggle('active');
    });
  });
});

function toggleFavorite(heartIcon) {
  if (heartIcon.style.color === "red") {
    heartIcon.style.color = "gray";
  } else {
    heartIcon.style.color = "red";
  }
}
function toggleFavorite(element) {

  element.classList.toggle("zoomIn");
}
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
