$(document).ready(function(){
  $('form#add').submit(function(event) {
    event.preventDefault();
    var self = $(this),
    postData = self.serializeArray();

    $.ajax({
        url : '/api/add/tag',
        type: 'POST',
        data : postData,
        success:function(answer) {
            console.log('на сервер успешно отправлены данные в виде: %s', JSON.stringify(postData))
            /// ответ от сервера console.log('----------------------------------/n' + JSON.stringify(answer))

        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});