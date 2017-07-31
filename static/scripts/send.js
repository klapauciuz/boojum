/*Добавление и удаление тегов*/
$(document).ready(function(){
    if(document.URL.indexOf("add") >= 0){ 
        var arr = [];
        $( "#university" ).autocomplete({
            source: function( request, response ) {
                $.getJSON("/autocomplete", {
                    search: request
                }, function( data ) {
                    response($.map(data, function (item) {
                        console.log(item._id['$oid']);
                        if ( arr.indexOf( item._id['$oid'] ) > -1 ) {
                            return;
                        }
                        if(item.images[0]) {    
                            var icon = '/static/images/' + item.images[0].toString().split(",");
                        } else { var icon = ''}
                        return {
                            value: item.name.toString().split(","),
                            label: item.name.toString().split(","),
                            id: item._id,
                            icon: icon
                        };
                    }));

                    });
            },
            select: function (e, ui) {
                console.log(ui.item.label[0] + ':' + ui.item.id['$oid']);
                $('.llinked-obj').append('<li>' + ui.item.label[0] + '</li>');
                $(this).val(''); 
                arr.push(ui.item.id['$oid']);
                return false;
            },
            minLength: 2,
            }).data("ui-autocomplete")._renderItem = function (ul, item) {
                console.log(item);
                return $( "<li></li>" )
                    .data("ui-autocomplete-item", item)
                    .append("<a class='trigger' maxlength='10'>" + item.label + "<img src='" + item.icon + "' /></a>")
                    .appendTo(ul);
        };
        $('form#add').submit(function(event) {
            event.preventDefault();
            var self = $(this),
            postData = self.serializeArray();
            postData.push({ name: "objects", value: arr });
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
    }
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

