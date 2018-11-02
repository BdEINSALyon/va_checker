from django import forms

class AddCheckForm(forms.Form):
    card_number = forms.CharField(max_length=13,required=True)