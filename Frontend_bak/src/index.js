const $ = require('jquery');




$(document).ready(function() {
    var html =
        '<div>' +
        '<input type="file" class="vFileField" id="avatar_file" />' +
        '<a href="javascript:void(0);" class="addlink" id="submit_avatar">点击上传</a>' +
        '</div>';

    $('.field-avatar_url p').append(html);

    $('#submit_avatar').click(function() {
        console.log('1111');
        //console.log($('#avatar_file'));
        //var avatar_file = $('#avatar_file').prop('files');
        //console.log(avatar_file);
    });
});

