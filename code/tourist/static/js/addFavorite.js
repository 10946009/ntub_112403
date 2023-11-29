function addFavorite(aid) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log("目前點擊的id為" + aid);
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        url: "/add_favorite/",
        data: {
            'id': aid,
        },
        success: function (response) {
            favorite_result = response.response_data["message"];
            if (favorite_result === "尚未登入") {
                alert("請先登入!")
                window.location.href = "/login";
            } else {
                changeFavorite(aid)
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
        }
    });
}
function changeFavorite(aid) {
    var favoriteButton = document.getElementById("submitfavorite" + aid);
    var isFavoriteValue = favoriteButton.getAttribute("data-isfavorite");
    if (isFavoriteValue === "1") {
        favoriteButton.innerHTML = '<i class="fas fa-heart" style="color: rgb(111, 110, 110); font-size: 16px;"></i>';
        favoriteButton.setAttribute("data-isfavorite", "0");
    } else {
        favoriteButton.innerHTML = '  <i class="fas fa-heart" style="color: rgb(202, 13, 13); font-size: 16px;"></i>';
        favoriteButton.setAttribute("data-isfavorite", "1");
    }
}
function addFavorite_index(id, type) {
    console.log("目前點擊的id為" + id);
    console.log("目前URL為" + type);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        url: type,
        data: {
            'id': id,
        },
        success: function (response) {

            favorite_result = response.response_data["message"];
            if (favorite_result === "尚未登入") {
                alert("請先登入!")
                window.location.href = "/login";
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);

        }
    });
}


function addFavorite_attractions(element,id) {
    console.log("目前點擊的id為" + id);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        url: "/add_favorite/",
        data: {
            'id': id,
        },
        success: function (response) {
            const favorite_heart = element.querySelector(".fa-heart");
            favorite_result = response.response_data["message"];
            if (favorite_result === "尚未登入") {
                alert("請先登入!")
                window.location.href = "/login";
            } else {
                if (favorite_heart.style.color === "rgb(202, 13, 13)") {
                    favorite_heart.style.color = "rgb(111, 110, 110)";
                } else {
                    favorite_heart.style.color = "rgb(202, 13, 13)";
                }
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);

        }
    });
}

function addFavorite_travel(element,id) {
    console.log("目前點擊的id為" + id);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        url: "/add_travel_favorite/",
        data: {
            'id': id,
        },
        success: function (response) {
            const favorite_heart = element.querySelector(".fa-heart");
            favorite_result = response.response_data["message"];
            if (favorite_result === "尚未登入") {
                alert("請先登入!")
                window.location.href = "/login";
            } else {
                // changeFavorite(id);
                if (favorite_heart.style.color === "rgb(202, 13, 13)") {
                    favorite_heart.style.color = "rgb(111, 110, 110)";
                } else {
                    favorite_heart.style.color = "rgb(202, 13, 13)";
                }
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);

        }
    });
}