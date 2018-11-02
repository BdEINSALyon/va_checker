from django.shortcuts import render
from .forms import AddCheckForm
from .models import CheckPlace

# Create your views here.
def add_check(request, pk):
    form = AddCheckForm(request.POST or None)
    check_place = CheckPlace.objects.get(pk=pk)
    form.fields['card_number'].widget.attrs.update({'autofocus': 'autofocus','required': 'required', 'placeholder': 'cXXXXXXXXXXXX'})
    if form.is_valid():
        member = form.cleaned_data['member']
    return render(request, 'checker/add_check_form.html', {'form': form, 'place':check_place})