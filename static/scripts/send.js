$(document).ready(function(){
  $('form#add').submit(function(event) {
    event.preventDefault();
    var self = $(this),
    postData = self.serializeArray();

    $.ajax({
        url : '/api/add/tag',
        type: 'POST',
        data : postData,
        success:function() {
            console.log('на сервер успешно отправлены данные в виде: %s', JSON.stringify(postData))
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});