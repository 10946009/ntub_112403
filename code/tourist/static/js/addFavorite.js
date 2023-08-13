function addFavorite(aid){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    alert( csrftoken )
    $.ajax({
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        url: "/add_favorite/",
        data: {
            'aid': aid,
        },
        success: function(data) {
            console.log(data);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
        }
    });
}

// const form = document.getElementById('addFavorite')
// form.addEventListener('submit', () => {
//     event.preventDefault() // 新增此行
//   })