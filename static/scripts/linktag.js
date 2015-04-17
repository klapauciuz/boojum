$(document).ready(function(){
  $('#add_linked_tag').click(function(event) {
    event.preventDefault();
    var self = $(this);
    var objName = $('h2').text();
<<<<<<< HEAD
    var data = self.serializeArray();
=======
    var data = {
          data: JSON.stringify({
                            "value": $('option:selected').val(),
                            "name": $('option').text()
                        })
       };
>>>>>>> 3cf61edf5a0e9b48a4d9a31abe0390c490e1affa
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