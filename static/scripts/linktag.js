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
            if('{{show_tags}}'.length != 0) {
                $('.linked p').hide()
            }
            console.log(data);
            var iiii = $('<a class="new" href="/tags/'+tagsNames+'">'+tagsNames+'</a>');
            $('.linked_box_in_object .linked').append(iiii);
            $(iiii).fadeTo('slow', 1);
            $(iiii).hover(function() {
                $(this).removeClass('new');
            });
            setTimeout(function() {
                $(iiii).removeClass('new');
            }, 2000);
        },
        error: function(err) {
          console.log(JSON.stringify(err));
        }
    });
  })
});