function addFavorite(aid) {
    var favoriteButton = document.getElementById("submitfavorite" + aid);
    var isFavoriteValue = favoriteButton.getAttribute("data-isfavorite");
    if (isFavoriteValue === "1") {
        favoriteButton.innerHTML = '<i class="fa-regular fa-heart"></i>&ensp;收藏';
        favoriteButton.setAttribute("data-isfavorite", "0");
    } else {
        favoriteButton.innerHTML = '<i class="fa-solid fa-heart"></i>&ensp;已收藏';
        favoriteButton.setAttribute("data-isfavorite", "1");
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        url: "/add_favorite/",
        data: {
            'aid': aid,
        },
        success: function (data) {
            console.log(data);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
        }
    });
}