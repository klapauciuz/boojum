/*Прикрепление тегов к объекту*/
$(document).ready(function(){
  $('#add_linked_tag').click(function(event) {
    event.preventDefault();
    var self = $(this);
    var objName = $('h2').text();
    var tagsValues = $('ul.options').find('li.selected').map(function (i,el) {
      return $(el).data('val');
    }).get();

    console.log(tagsValues);
    console.log($('p.CaptionCont span').text());
    
    var data = {
          data: JSON.stringify({
                            "values": tagsValues,
                            "names": $('p.CaptionCont span').text()
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