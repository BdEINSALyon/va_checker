from datetime import timedelta

from django import forms
from django.utils.datetime_safe import datetime


class AddCheckForm(forms.Form):
    card_number = forms.CharField(max_length=13, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Numéro de carte VA'}))


def debut_ce_mois():
    today = datetime.today()
    return today - timedelta(days=today.day - 1)


def fin_ce_mois():
    return debut_ce_mois() + timedelta(days=30)


class FilterForm(forms.Form):
    class Meta:
        pass

    start = forms.DateTimeField(initial=debut_ce_mois, required=True, label="Début",
                                widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type':'date'}))
    end = forms.DateTimeField(initial=fin_ce_mois, required=True, label="Fin",
                              widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type':'date'}))
    prec = forms.CharField(initial='.') # sert à stocker le referer pour les écrans de scan tactiles
