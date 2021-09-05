$(document).ready(function(){

  // init FlexSlider
  // ------------------------------------------------------------------------
  $('.flexslider').flexslider({
    slideshow: true,
    directionNav: false
  });

  // Cart (placeholder) Change/edit this function as needed
  // ------------------------------------------------------------------------
  // $(".product-remove").on('click', function(e) {
  //   $(this).parent(".cart-item").fadeOut("slow");
  //   e.preventDefault();
  // }); 

  // Toggle search
  // ------------------------------------------------------------------------
  $(".reveal-search").on('click', function(e) {
    $(".search-wrapper").addClass("show-search");
    $(".search-form input:text").first().focus();
    e.preventDefault();
  });

  /*esc button to close search*/
  // if($('.search-wrapper').hasClass('show-search')) {
    $('body').keydown( function( event ) {
      if ( event.which == 27 ) {
        $(".search-wrapper").removeClass("show-search");
      }
    });
  // }       

  // Styled drop down
  // ------------------------------------------------------------------------
  $('.styled-drop-down').dropkick();

  // Toggle Main Nav (smaller screens)
  // ------------------------------------------------------------------------
  $(".toggle-nav").on('click', function(e) {
    $(".main-nav, .header-controls").slideToggle("slow");
    e.preventDefault();
  });  

  // Toggle Main Nav (smaller screens)
  // ------------------------------------------------------------------------
  // var $container = $('.sortable-grid');
  // // init
  // $container.isotope({
  //   // options
  //   itemSelector: '.grid-item',
  //   layoutMode: 'fitRows'
  // });  

});

// window.onresize = function(event) {
//   // $('.styled-drop-down').dropkick();
// };