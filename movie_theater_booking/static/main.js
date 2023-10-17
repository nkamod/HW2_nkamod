// On page load
$(document).ready(function() {
    let pathname = window.location.pathname;
    
    // TODO: Implement active nav item functionality (Highligh active nav item)

    // select next slide button
    const slides = $(".slide");

    slides.each(function(index) {
        $(this).css("transform", `translateX(${index * 100}%)`)
    });

    // current slide counter
    let curSlide = 0;
    // maximum number of slides
    let maxSlide = slides.length - 1;

    $(".btn-next").on("click", function () { 
        // check if current slide is the last and reset current slide
        if (curSlide === maxSlide) {
            curSlide = 0;
        } else {
            curSlide++;
        }

        slides.each(function(index) {
            $(this).css("transform", `translateX(${100 * (index - curSlide)}%)`);
        });
    });

    $(".btn-prev").on("click", function () {
        // check if current slide is the first and reset current slide to last
        if (curSlide === 0) {
          curSlide = maxSlide;
        } else {
          curSlide--;
        }
      
        //   move slide by 100%
        slides.each(function(indx) {
            $(this).css("transform", `translateX(${100 * (indx - curSlide)}%)`);
        });
    });

})



