function addFavorite(aid) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        url: "/add_favorite/",
        data: {
            'aid': aid,
        },
        success: function (response) {
            favorite_result = response.response_data["message"];
            if(favorite_result==="尚未登入"){
                alert("請先登入!")
                window.location.href = "/login";
            }else{
                var favoriteButton = document.getElementById("submitfavorite" + aid);
                var isFavoriteValue = favoriteButton.getAttribute("data-isfavorite");
                if (isFavoriteValue === "1") {
                    favoriteButton.innerHTML = '<i class="fa-regular fa-heart"></i>&ensp;收藏';
                    favoriteButton.setAttribute("data-isfavorite", "0");
                } else {
                    favoriteButton.innerHTML = '<i class="fa-solid fa-heart"></i>&ensp;已收藏';
                    favoriteButton.setAttribute("data-isfavorite", "1");
                }
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
        }
    });
}

function addFavorite_index(id,type) {
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
            if(favorite_result==="尚未登入"){
                alert("請先登入!")
                window.location.href = "/login";
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);

        }
    });
}