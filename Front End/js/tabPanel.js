$('nav a').click(function(event) {
  event.preventDefault();

  var target = $(this).attr('href');

  // the .not() makes it so if we are on that page, it doesn't fade in and out the same content
  $('.content:visible').not(target).fadeOut('slow', function() {
    // after we fade out old content, fade in new
    $(target).fadeIn('slow');
  });
});
