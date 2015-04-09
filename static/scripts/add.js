$(document).ready(function(){
  $('#add_tag').click(function(event) {
    event.preventDefault();
    var self = $(this),
    tagName = $('h2').text();
    $.ajax({
        url : '/'+tagName,
        type: 'POST',
        data : tagName,
        success:function(response) {
            self.animate({
                opacity: 0,
          }, 400, function() {
            self.val('success!');
            self.css('cursor', 'default');
            self.animate({
                opacity: 1,
            });
            self.attr('disabled', 'disabled');
          });
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});