$(document).ready(function() {
  $('.read-more-btn').click(function() {
    var $shortText = $(this).siblings('.short-text');
    var $fullText = $(this).siblings('.full-text');

    if ($shortText.is(':visible')) {
      $shortText.hide();
      $fullText.show();
      $(this).text('Skaityti mažiau');
    } else {
      $fullText.hide();
      $shortText.show();
      $(this).text('Skaityti daugiau');
    }
  });
});
