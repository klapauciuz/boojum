$(document).ready(function(){
    $('#upload-file').change(function(){
        var formData = new FormData();
        formData.append('section', 'general');
        formData.append('action', 'previewImg');
        formData.append('image', $('input[type=file]')[0].files[0]); 
        formData.append('id', object_id);
        $.ajax({
            type: 'POST',
            url: '/upload',
            processData: false, // important
            contentType: false, // important
            dataType : 'json',
            data: formData,
            success: function(data) {
                console.log('Success upload ' + $('input[type=file]')[0].files[0].name + ' to with ' + object_id);
                var grid = document.querySelector('#grid');
                    var item = document.createElement('a');
                    var item2= document.createElement('img');
                    item.setAttribute("href", "/static/images/"+ $('input[type=file]')[0].files[0].name)
                        item.setAttribute("target", "_blank");
                            item2.setAttribute("src", "/static/images/"+ $('input[type=file]')[0].files[0].name);
                                item.appendChild(item2);
                                    salvattore.appendElements(grid, [item]);
            },
        });
    })
});