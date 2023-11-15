// 輪播套件
function owlStart(){
    $('.owl-carousel').owlCarousel({
        items: 4,
        loop: true,
        margin: 10,
        dots: false,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            600: {
                items: 3
            },
            1000: {
                items: 4
            }
        }
    });
}