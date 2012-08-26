# -*- coding: UTF-8 -*-

from django import forms
from agri import settings
from django.utils.safestring import mark_safe

class ColorWidget(forms.widgets.TextInput):

    def render(self, name, value, attrs=None):
        text_input_html = super(ColorWidget, self).render(name, value, attrs)
        text_link_html = u'<a id="id_color_picker" href="#" onclick="return false;">%s</a>' % u'Палитра'
        return mark_safe('%s %s' % (text_input_html, text_link_html) +  mark_safe(u'''<div id='colorpicker'></div>
                <link href="/stylesheets/farbtastic.css" rel="stylesheet" type="text/css" />
                <script type="text/javascript" src="/javascripts/farbtastic.js"></script>
                <script type="text/javascript">
                    var picker_widget = "<div id='colorpicker'></div>";
                    var id_color = $('#id_%(name)s');
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
                </script>'''%{'name': name}))

    class Media:
        css = {
                'all': (settings.MEDIA_ROOT + 'stylesfeets/farbtastic.css',)
              }
        js = (settings.MEDIA_ROOT + "javascripts/farbtastic.js",)