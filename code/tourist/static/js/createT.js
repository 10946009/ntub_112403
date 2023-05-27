// $(function(){
//     $('#contents div[id != "tab_c"]').hide();

// });

$(function(){
    var navPos = $("nav").offset().top;

    $(window).scroll(function(){
        if($(window).scrollTop()>navPos){
            $("nav").css("postion","fixed");
        }else{
            $("nav").css("postion","static");
        };
    })
});