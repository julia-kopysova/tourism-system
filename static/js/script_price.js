$(document).ready(function() {
  // проверка готовности использования кода,выполнять внутри
  $(".owl-carousel").owlCarousel({
    // карусель прокручивается бесконечно
    margin: 10,

    nav: true, // навигация есть
    navClass: ["slider__nav--left", "slider__nav--right"],
    responsive: {
      //настройка адаптива
      0: {
        // на маленьких экранах
        items: 1 // по одному слайду
      },

      800: {
        // от 600 пикселей
        items: 2
      },

	   1200: {
        // на маленьких экранах
        items: 3 // по одному слайду
      },
    }
  });
});
