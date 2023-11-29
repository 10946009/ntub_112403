// //詳細景點資訊幻燈片圖
// var slideIndex1 = 1;
// showSlides(slideIndex1);
// function plusSlides(n) {
//   showSlides((slideIndex1 += n));
// }
// function currentSlide(n) {
//   showSlides((slideIndex1 = n));
// }
// function showSlides(n) {
//   let i;
//   let slides = document.getElementsByClassName("mySlides"); // 取得所有幻燈片元素
//   if (n > slides.length) {
//     slideIndex1 = 1;
//   } // 當索引超出最大值時，將索引設為第一張幻燈片
//   if (n < 1) {
//     slideIndex1 = slides.length;
//   } // 當索引小於1時，將索引設為最後一張幻燈片
//   for (i = 0; i < slides.length; i++) {
//     slides[i].style.display = "none"; // 隱藏所有幻燈片
//   }

//   slides[slideIndex1 - 1].style.display = "block"; // 顯示目前索引對應的幻燈片
// }

//簡單景點介紹js幻燈片
var slideIndex = 1;
show_start(slideIndex);
function plusDivs(n, name) {
  showDivs((slideIndex += n), name);
}
function showDivs(n, name) {
  var i;
  var selector = `[name="${name}"]`;
  var x_imgs = document.getElementsByClassName("slide");
  var x = [];
  for (i = 0; i < x_imgs.length; i++) {
    var dataName = x_imgs[i].dataset.name;
    if (dataName === name) {
      x.push(x_imgs[i]); // 將符合條件的元素存入 x 陣列
    }
  }
  if (n > x.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = x.length;
  }
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none"; // 隱藏所有元素
  }
  x[slideIndex - 1].style.display = "block"; // 顯示目前索引對應的元素
}

function show_start(n) {
  var i;
  var x = document.getElementsByClassName("slide");
  if (n > x.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = x.length;
  }
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none"; // 隱藏所有元素
  }
  var xArray = Array.from(x);
  var showList = [];
  var checkList = [];
  xArray.forEach((xslide) => {
    const dataName = xslide.getAttribute("data-name");
    if (!checkList.includes(dataName)) {
      checkList.push(dataName);
      xslide.style.display = "block"; // 顯示起始索引對應的元素
    }
  });
}
