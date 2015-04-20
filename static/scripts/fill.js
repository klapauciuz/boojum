$(document).ready(function(){
    
  $('tags.fill').click(function(event) {
    event.preventDefault();
    var self = $(this),
    postData = self.serializeArray();

    $.ajax({
        url : '',
        type: 'POST',
        data : postData,
        success:function(response) {
            window.location.replace("/");
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});