$(document).ready(function(){
  $('#add_tag').click(function(event) {
    event.preventDefault();
    var self = $(this),
    tagName = $('h2').text();
    $.ajax({
        url : '/'+tagName,
        type: 'POST',
        data : tagName,
        success:function(response) {
            $('#add_tag').val('success!');
            
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});