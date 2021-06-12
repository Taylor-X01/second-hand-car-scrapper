from django import forms


class Fields(forms.Form):
    mark = forms.CharField(label='mark', max_length=100)
    model = forms.CharField(label='model', max_length=100)
    year = forms.CharField(label='year', max_length=100)
    km = forms.CharField(label='km', max_length=100)
    city = forms.CharField(label='city', max_length=100)
