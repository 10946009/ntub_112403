// 輪播套件
function similarOwl(){
    $('.owl-carousel').owlCarousel({
        items: 5,
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
            650: {
                items: 3,
                slideBy:3
                
            },
            700: {
                items: 4,
                slideBy: 4
            }
        }
    });
}