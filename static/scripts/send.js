/*Добавление и удаление тегов*/
$(document).ready(function(){
    $('form#add').submit(function(event) {
        event.preventDefault();
        var self = $(this),
        postData = self.serializeArray();

        $.ajax({
            url : '/tags/add',
            type: 'POST',
            data : postData,
            success:function(response) {
                console.log(response);
                window.location.replace("/tags/"+response);
            },
            error: function(err) {
              console.log(JSON.stringify(err));
            }
        });
    });
    $('#delete').click(function(event) {
        event.preventDefault();
        var self = $(this),
        tagName = $('h2').text();
        $.ajax({
            url : '/tags/'+tagName,
            type: 'DELETE',
            success:function(response) {
                window.location.replace("/");
            },
            error: function(err) {
              console.log(JSON.stringify(err));
            }
        });
    });
    $('form#add_fromwiki').submit(function(event) {
        event.preventDefault();
        var self = $(this),
        postData = self.serializeArray();
        $('#wide_submit').val('loading');
        $('#wide_submit').prop('disabled', true);
        $('#wide_submit').css('cursor', 'progress');
        $('#wide_submit').animate({
                opacity: 0.2,
        });
        console.log(postData);
        
        $.ajax({
            url : '/objects/add',
            type: 'POST',
            data : postData,
            success:function(response) {
                console.log(response);
                window.location.replace(response);
            },
            error: function(err) {
                console.log(JSON.stringify(err));
            }
        });
    });
});

