$(document).ready(function(){
  $('.tags .fill').click(function(event) {
    if( !confirm('It will fill your scopes by linked scopes from all objects. Ok?') ) 
            return;
    var self = $(this);
    $.ajax({
        url : '/collection/tags/fill',
        type: 'POST',
        success:function(response) {
            location.href = '/collection'
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  });
  $('.objects .fill').click(function(event) {
    if( !confirm('It will fill your objects by linked objects from all scopes. Ok?') ) 
            return;
    var self = $(this);
    $.ajax({
        url : '/collection/objects/fill',
        type: 'POST',
        success:function(response) {
            location.href = '/collection'
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});