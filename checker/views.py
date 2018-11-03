from django.shortcuts import render
from .forms import AddCheckForm
from .models import CheckPlace, Check
from checker.adhesion_api import AdhesionAPI
from django.utils import timezone

# Create your views here.
def add_check(request, pk):
    form = AddCheckForm(request.POST or None)
    check_place = CheckPlace.objects.get(pk=pk)
    form.fields['card_number'].widget.attrs.update({'autofocus': 'autofocus','required': 'required', 'placeholder': 'cXXXXXXXXXXXX'})
    res={}
    if form.is_valid():
        res['state']=True
        card_number = form.cleaned_data['card_number']
        res['card_number']=card_number
        api=AdhesionAPI()
        card=api.get_infos_card(card_number)
        if(card is not None):
            res['first_name'] = card['first_name']
            res['last_name'] = card['last_name']
            res['gender'] = card['gender']
            if card['valid_member']:
                check = Check()
                try:
                    passage = Check.objects.filter(student_id=card['member']).filter(check_place=check_place).latest('created_at')
                    res['last_seen'] = passage.created_at
                    delta_minutes=(timezone.now() - passage.created_at).seconds // 60
                    if(delta_minutes<check_place.legit_delta):
                        res['state'] = "seemsnotlegit"
                        check.seems_legit=False
                    else:
                        res['state'] = "seemslegit"
                        check.seems_legit=True
                except Check.DoesNotExist:
                    passage = None
                    res['last_seen'] = None
                    res['state'] = "seemslegit"
                    check.seems_legit = True
                check.student_id = card['member']
                check.card_number = card_number
                check.check_place = check_place
                check.save()
                request.POST = None
                form = AddCheckForm(None)
                form.fields['card_number'].widget.attrs.update({'autofocus': 'autofocus', 'required': 'required', 'placeholder': 'cXXXXXXXXXXXX'})
            else:
                res['state'] = "notvamember"
        else:
            res['state'] = "cardnotfound"
    else:
        res['state']="begin"
    return render(request, 'checker/add_check_form.html', {'form': form, 'place':check_place, 'res':res})