$(document).ready(function(){
  $('#add_linked_tag').click(function(event) {
    event.preventDefault();
    var self = $(this);
    var objName = $('h2').text();
    var data = {
          data: JSON.stringify({
                            "value": $('option').val()
                        })
       };
    $.ajax({
        url : '/objects/'+objName,
        type: 'POST',
        data: data,
        success:function(response) {
            console.log(data);
            window.location.replace('/objects/'+objName);
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});