document.addEventListener('DOMContentLoaded', function() {
  const locationHearts = document.querySelectorAll('.location-heart');

  locationHearts.forEach(function(heart) {
    heart.addEventListener('click', function() {
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
