var $ = django.jQuery;
alert("aaaaaaaaa")
var picker_widget = "<div id='colorpicker'></div>";

$(document).ready(function() {
    alert("aaaaaaaaa")

    var id_color = $('#id_color');
    $(picker_widget).appendTo('body');
    $('#id_color_picker').bind('click', function() {
        var offset = id_color.offset();
        var helper_style = {
            'top': offset.top + id_color.height() + 3,
            'left': offset.left,
            'opacity': 0.9,
        };
        $('#colorpicker').css(helper_style).toggle(400);
    });
    $('#colorpicker').hide().farbtastic(id_color);
});