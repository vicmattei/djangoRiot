from django import forms


class SummonerSearchForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
