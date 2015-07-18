$(document).ready(function(){
    $('#upload-file').change(function(){
        $(this).submit();
        var form_data = new FormData($('#upload-file')[0]);
        form_data.append('id', object_id);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(data) {
                console.log('Success upload image to with ' + object_id);
                location.reload();
            },
        });
    })
});