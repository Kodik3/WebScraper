from django import forms


class MainForm(forms.Form):
    url = forms.URLField()