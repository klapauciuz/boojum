/*Прикрепление тегов к объекту*/
$(document).ready(function(){
  $('#add_linked_tag').click(function(event) {
    if ($('.yeah').val() == null) 
    {
      $('.placeholder').append('!');
      return false;
    }
    event.preventDefault();
    var self = $(this);
    var objName = $('h2').text();
    var tagsValues = $('ul.options').find('li.selected').map(function (i,el) {
      return $(el).data('val');
    }).get();

    var tagsNames = $('p.CaptionCont span').text().split(',');
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
            $('#add_linked_tag').css('opacity', 0);
            for (x=0;x<tagsNames.length;x++) {  
              tagsNames[x] = $.trim(tagsNames[x]);
              $('.linked_box_in_object .linked').append('<a class="new" href="/tags/'+tagsNames[x]+'">'+tagsNames[x]+'</a>');
            }

            $('.new').fadeTo('slow', 1);
            
            var obj = [];
            $('option:selected').each(function () {
                obj.push($(this).index());
            });
            for (var i = 0; i < obj.length; i++) {
                $('.yeah')[0].sumo.unSelectItem(obj[i]);
                $('.yeah')[0].sumo.disableItem(obj[i]);
            }
            $('.CaptionCont span').addClass('placeholder').text('...another one?');
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