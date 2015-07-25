/*Добавление/удаление в личной коллекции*/
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
            self.animate({
                    opacity: 0,
              }, 120, function() {
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

$('#add_obj').on('click', function(event) {
    event.preventDefault();
    var self = $(this),
    objName = $('h2').text();
    $.ajax({
        url : '/objects/'+objName,
        type: 'POST',
        data : objName,
        success:function(response) {
                repl = $('<div id="del_obj" class="universal_button" type="submit"><img src="/static/post_old.gif"> remove from collection</div>')
                self.replaceWith( repl );
            },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  });
    $('#del_obj').on('click', function(event) {
        event.preventDefault();
        var self = $(this),
        objName = $('h2').text();
        $.ajax({
            url : '/objects/'+objName,
            type: 'POST',
            data : objName,
            success:function(response) {
                repl = $('<div id="add_obj" class="universal_button" type="submit"><img src="/static/post_new.gif"> add to your collection</div>')
                self.replaceWith( repl );
            },
        });
  });
});