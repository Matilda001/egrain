from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from models import HistoryCornfield, Agriculture, Manure
from field import ColorWidget
import re

class ModelForm(ModelForm):

    def as_div(self):
        return self._html_output(
            error_row = u'<div class="error">%s</div>',
            normal_row = u'<div%(html_class_attr)s><div class="form-label">%(label)s</div> %(field)s %(help_text)s %(errors)s</div> ',
            row_ender = u'</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)




class AuthenticationForm1(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'text_input_login'}), label = "E-mail")
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput(attrs={'class':'text_input_login'}))

class FormHistoryCornfield(ModelForm):
    manure = forms.ModelChoiceField(label=u'Удобрения', queryset = Manure.objects.all(), empty_label="", widget=forms.Select, required=False)

    class Meta:
        model = HistoryCornfield
        #exclude = ('cornfield')

class FormAgriculture(ModelForm):
    class Meta:
        model = Agriculture
        widgets = {
            'color_agriculture': ColorWidget(attrs={'value':'#ffffff','readonly': "readonly"}),
            }

    def clean_color_agriculture(self):
        value = self.cleaned_data['color_agriculture']
        if not re.match('#[0-9a-fA-F]{6}', value):
            raise forms.ValidationError(self.error_messages['invalid'])
        return value

class FormManure(ModelForm):
    class Meta:
        model = Manure
        exclude = ('field_manure')

class AddField(forms.Form):
    append_field = forms.FileField(label="Добавить *.kml файл", widget=forms.FileInput(attrs={'accept': "text/kml"}) )