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
                window.location.replace("/");
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

        $.ajax({
            url : '/objects/add',
            type: 'POST',
            data : postData,
            success:function(response) {
                console.log(response);
                window.location.replace("/objects/" + response);
            },
            error: function(err) {
              console.log(JSON.stringify(err));
            }
        });
    });
});

