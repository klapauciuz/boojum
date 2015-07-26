/*Добавление/удаление в личной коллекции*/
$(document).ready(function(){
$('#add_tag, #del_tag').on('click', function(event) {
    event.preventDefault();
    var self = $(this),
    tagName = $('h2').text(),
    speed = 120;
    $.ajax({
        url : '/tags/'+tagName,
        type: 'POST',
        data : tagName,
        success:function(response) {
             if (self.hasClass('add')) {
                console.log('add');
                self.fadeTo(speed, 0, function() {
                    self.toggleClass('add del').attr("id","del_tag").html('<img src="/static/post_old.gif"> remove from collection');
                });
                self.fadeTo(speed, 1);

            } else {
                console.log('del');
                self.fadeTo(speed, 0, function() {
                    self.toggleClass('del add').attr("id","add_tag").html('<img src="/static/post_new.gif"> add to your collection');                
                });
                self.fadeTo(speed, 1);
            }
            },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
});
$('#add_obj, #del_obj').on('click', function(event) {
    event.preventDefault();
    var self = $(this),
    objName = $('h2').text(),
    speed = 120;
    $.ajax({
        url : '/objects/'+objName,
        type: 'POST',
        data : objName,
        success:function(response) {
             if (self.hasClass('add')) {
                console.log('add');
                self.fadeTo(speed, 0, function() {
                    self.toggleClass('add del').attr("id","del_obj").html('<img src="/static/post_old.gif"> remove from collection');
                });
                self.fadeTo(speed, 1);

            } else {
                console.log('del');
                self.fadeTo(speed, 0, function() {
                    self.toggleClass('del add').attr("id","add_obj").html('<img src="/static/post_new.gif"> add to your collection');                
                });
                self.fadeTo(speed, 1);
            }
            },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
});
});