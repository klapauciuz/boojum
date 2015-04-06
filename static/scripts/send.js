$(document).ready(function(){
  $('form#add').submit(function(event) {
    event.preventDefault();
    var self = $(this),
    postData = self.serializeArray();

    $.ajax({
        url : '/api/add/tag',
        type: 'POST',
        data : postData,
        success:function(response) {
            console.log('на сервер успешно отправлены данные в виде: %s/n', JSON.stringify(postData))
            console.log('ответ сервера: %s', JSON.stringify(response))
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});