from django import forms
from .models import Currency
import datetime


class SelectCurForms(forms.Form):
    main = forms.ModelChoiceField(
        Currency.objects.exclude(code='RUB'),
        to_field_name='code'
    )
    sub = forms.ModelChoiceField(
        Currency.objects.exclude(code='RUB'),
        to_field_name='code'
    )
    date_from = forms.DateField(initial=datetime.date.today())
    date_to = forms.DateField(initial=datetime.date.today())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'