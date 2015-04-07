$(document).ready(function(){
  $('form#signup').submit(function(event) {
    event.preventDefault();
    var self = $(this),
    postData = self.serializeArray();

    $.ajax({
        url : '/api/signup',
        type: 'POST',
        data : postData,
        success:function(response) {
            console.log(postData)
            $('form#signup').replaceWith("<h2>welcome, "+postData[0].value+"!</h2>")

        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});