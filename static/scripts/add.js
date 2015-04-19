$(document).ready(function(){
  $('#add_tag').click(function(event) {
    event.preventDefault();
    var self = $(this),
    tagName = $('h2').text();
    $.ajax({
        url : '/tags/'+tagName,
        type: 'POST',
        data : tagName,
        success:function(response) {
            self.animate({
                opacity: 0,
          }, 120, function() {
            /*self.text('success!');*/
            self.css('cursor', 'default');
            self.animate({
                opacity: 1,
            });

            self.prop('disabled', 'disabled');
            self.delay( 600 )
            window.location.replace('/tags/'+tagName);
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
            url : '/tags/'+tagName,
            type: 'POST',
            data : tagName,
            success:function(response) {

/*                self.css('opacity', '0');
*/               /* self.text(' ! ');*/
                /*self.delay( 300 );*/
                self.css('display','none');
                $('.already').delay(340);
                $('.already').animate({
                    opacity: 0,
                }, 120, function(){
                    
                    setTimeout(function () {
                        location.href = '/tags/'+tagName
                    }, 300);
                });
             
            },
            error: function(err) {
                console.log(JSON.stringify(err));
            }
        });
  });
$('#add_obj').click(function(event) {
    event.preventDefault();
    var self = $(this),
    objName = $('h2').text();
    $.ajax({
        url : '/collection/add/'+objName,
        type: 'POST',
        data : objName,
        success:function(response) {
            self.animate({
                opacity: 0,
          }, 120, function() {
            /*self.text('success!');*/
            self.css('cursor', 'default');
            self.animate({
                opacity: 1,
            });
            
            self.prop('disabled', 'disabled');
            self.delay( 600 )
            window.location.replace('/objects/'+objName);
          });
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  });
    $('#del_obj').click(function(event) {
        event.preventDefault();
        var self = $(this),
        objName = $('h2').text();
        $.ajax({
            url : '/collection/add/'+objName,
            type: 'POST',
            data : objName,
            success:function(response) {

/*                self.css('opacity', '0');
*/               /* self.text(' ! ');*/
                /*self.delay( 300 );*/
                self.css('display','none');
                $('.already').delay(340);
                $('.already').animate({
                    opacity: 0,
                }, 120, function(){
                    
                    setTimeout(function () {
                        location.href = '/objects/'+objName
                    }, 300);
                });
             
            },
            error: function(err) {
                console.log(JSON.stringify(err));
            }
        });
  });
});