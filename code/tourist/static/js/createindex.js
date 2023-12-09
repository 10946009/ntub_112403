
// 隨機背景
document.addEventListener("DOMContentLoaded", function () {
    var images = [
      '../static/images/IMG20220125115200.jpg',
      '../static/images/bg1.jpg',
      '../static/images/bg2.jpg',
      '../static/images/bg5.png',
      '../static/images/bg6.jpeg',
      '../static/images/bg7.png',
      '../static/images/bg8.jpg',
      '../static/images/jp_img.jpg',
    ]
  
    var randomIndex = Math.floor(Math.random() * images.length);
    var randomImg = images[randomIndex];
  
    var bgimg = document.getElementById("bgimg");
  
    bgimg.style.background = 'url(' + randomImg + ')';
    bgimg.style.backgroundRepeat = 'no-repeat';
    bgimg.style.backgroundSize = 'cover';
    bgimg.style.backgroundPosition = 'center';
    bgimg.style.opacity = '0.65';
    bgimg.style.position = 'relative';
    bgimg.style.zIndex = '100';
  })
  
  // Step1 單選
  const choiceClassLeft = document.getElementById('choiceClassLeft');
  const choiceClassRight = document.getElementById('choiceClassRight');
  
  let isPickClass = false;
  
  function pickClass(element){
    choiceClassLeft.classList.remove('pickClassColor');
    choiceClassRight.classList.remove('pickClassColor');
  
    element.classList.add('pickClassColor');
    isPickClass = true;
  }
  choiceClassLeft.addEventListener('click', function(){
    pickClass(choiceClassLeft);
  })
  choiceClassRight.addEventListener('click', function(){
    pickClass(choiceClassRight);
  })
  // step1 to step2 
  function nextStep(){
    if(isPickClass){
      $('#step1').fadeOut(100,function(){
        $('#step2').fadeIn(500);
      });
    }else{
      $('#notion').css('display','block');
      // notion.style.display = 'block';
    }
  }
  // step2 to step1
  function backStep(){
    if(isPickClass){
      $('#step2').fadeOut(100,function(){
        $('#step1').fadeIn(500);
      });
    }
  }