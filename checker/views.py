from django.db.models import Count
from django.db.models.functions import TruncHour, TruncQuarter, TruncMinute
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView, FormView
from django.views.generic.base import ContextMixin

from checker.adhesion_api import AdhesionAPI
from .forms import AddCheckForm, FilterForm, debut_ce_mois, fin_ce_mois
from .models import CheckPlace, Check, Screen


@cache_control(must_revalidate=True, no_store=True)
def add_check(request, pk, screen_token=None):
    form = AddCheckForm(request.POST or None)
    check_place = CheckPlace.objects.get(pk=pk)
    if screen_token is None:
        url_refresh = reverse("add_check", args=[check_place.pk])
    else:
        url_refresh = reverse("screen", args=[screen_token])
    res={}
    if form.is_valid():
        res['state']=True
        card_number = form.cleaned_data['card_number']
        form = AddCheckForm(None) #On clean directement un formulaire vide
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
                    delta_minutes = timezone.now() - passage.created_at
                    if delta_minutes.total_seconds() < check_place.legit_delta * 60:
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
            else:
                res['state'] = "notvamember"
        else:
            res['state'] = "cardnotfound"
    else:
        res['state']="begin"
    return render(request, 'checker/add_check_form.html',
                  {'form': form, 'place': check_place, 'res': res, 'url_refresh': url_refresh})


@cache_control(must_revalidate=True, no_store=True)
def screen(request, token_screen):
    screen = Screen.objects.filter(token=token_screen)
    if screen.count() == 1:
        return add_check(request, screen[0].check_place.pk, screen[0].token)
    else:
        return render(request, 'checker/display_new_screen.html', {"token": token_screen})

def stats(request, checkplace:int):
    qs = Check.objects.filter(check_place=checkplace)
    if request.method=='GET':
        qs = qs.filter(created_at__month=localtime().month)
        form = FilterForm(initial={'prec':request.META.get('HTTP_REFERER','')}) # quand on filtre, ça se rajoute à l'historique, donc c'est chiant pour les écrans de scan
    elif request.method=='POST':
        form = FilterForm(request.POST)
        form.is_valid()
        qs = qs.filter(created_at__gte=form.cleaned_data.get('start', debut_ce_mois()), created_at__lte=form.cleaned_data.get('end',fin_ce_mois()))
    return render(request, 'checker/stats.html', {
        'form':form,
        'place':CheckPlace.objects.get(id=checkplace),
        'checks':qs.annotate(hour=TruncHour('created_at')).values('hour').annotate(total=Count('id')).order_by('hour')
    })