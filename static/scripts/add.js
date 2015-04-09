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
            /*self.text('success!');*/
            self.css('cursor', 'default');
            self.animate({
                opacity: 1,
            });
            self.prop('disabled', 'disabled');
            self.delay( 600 )
            window.location.replace('/'+tagName);
          });
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  });
    $('#del_tag').click(function(event) {
        event.preventDefault();
        var self = $(this),
        tagName = $('h2').text();
        $.ajax({
            url : '/'+tagName,
            type: 'POST',
            data : tagName,
            success:function(response) {
                self.css('opacity', '0');
               /* self.text(' ! ');*/
                self.delay( 300 );
                self.animate({
                    opacity: 0,
                }, 300, function(){
                    window.location.replace('/'+tagName);
                });
                /*self.delay( 600 )*/
             
            },
            error: function(err) {
                console.log(JSON.stringify(err));
            }
        });
  });
});