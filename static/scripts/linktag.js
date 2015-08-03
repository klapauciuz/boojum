/*Прикрепление тегов к объекту*/
$(document).ready(function(){
  $('.linked_new a').click(function(event) {
    event.preventDefault();
    var self = $(this);
    var objName = $('h2').text();
    /* 

    var tagsValues = $('ul.options').find('li.selected').map(function (i,el) {
    return $(el).data('val');
    }).get();

    var tagsNames = $('p.CaptionCont span').text().split(',');

    */
    tagsValues = [$(this).attr('value')];
    tagsNames = $(this).text();
    console.log(tagsValues, ':', tagsNames)
    $(this).hide();
    var data = {
          data: JSON.stringify({
                            "values": tagsValues,
                            "names": tagsNames
                        })
       };
    $.ajax({
        url : '/objects/'+objName,
        type: 'POST',
        data: data,
        success:function(response) {
            console.log(data);
            $('.linked_box_in_object .linked').append('<a class="new" href="/tags/'+tagsNames+'">'+tagsNames+'</a>');
            $('.new').fadeTo('slow', 1);
            $('.new').hover(function() {
              $(this).removeClass('new');
            });
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});