// 輪播套件
function indexOwl(){
    $('.owl-carousel').owlCarousel({
        items: 4,
        loop: false,
        margin: 10,
        dots: false,
        nav: true,
        responsive: {
            0: {
                items: 1,
                slideBy:1
            },
            500: {
                items: 2,
                slideBy:2
            },
            750: {
                items: 3,
                slideBy:3
                
            }
        }
    });
}