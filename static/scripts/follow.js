$(document).ready(function(){
  $('.followstatus').click(function(event) {
    event.preventDefault();
    var self = $(this);
    $.ajax({
        type: 'POST',
        data : userName,
        success:function(response) {
            self.animate({'opacity': 0}, 300);
            window.location.replace('/users/'+userName);
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  });
  $('.unfollow').click(function(event) {
    event.preventDefault();
    var self = $(this);
    $.ajax({
        type: 'DELETE',
        data : userName,
        success:function(response) {
            self.animate({'opacity': 0}, 300);
            window.location.replace('/users/'+userName);
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  });
});