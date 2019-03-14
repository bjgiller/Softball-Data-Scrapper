from django import forms

class TeamSearch(forms.Form):
    team = forms.CharField(label='Search Team Name', max_length=300, widget=forms.TextInput(attrs={'id': 'searchBar', 'type': 'text', 'name': 'myTeam', 'placeholder': 'Team Name'}))