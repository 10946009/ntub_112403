// 輪播套件
function owlStart(){
    $('.owl-carousel').owlCarousel({
        items: 6,
        loop: false,
        margin: 10,
        dots: false,
        nav: true,
        responsive: {
            0: {
                items: 1,
                slideBy:1
            },
            576: {
                items: 2,
                slideBy:2
            },
            600: {
                items: 3,
                slideBy:3
                
            },
            1000: {
                items: 5,
                slideBy:5
            }
        }
    });
}