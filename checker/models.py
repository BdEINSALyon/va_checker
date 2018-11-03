from django.db import models

# Create your models here.

class CheckPlace(models.Model):
    name = models.CharField(verbose_name='Nom', blank=False, max_length=255, null=False)
    is_active = models.BooleanField(verbose_name="Actif ?", default=True)
    legit_delta = models.IntegerField(verbose_name="Temps min en minutes entre 2 passage", blank=False, null=False)
    def __str__(self):
        return self.name
    @property
    def nombre_passage(self):
        return self.checks.count()

class Check(models.Model):
    student_id = models.IntegerField(verbose_name="ID sur Adhésion", blank=True, null=True)
    card_number = models.CharField(verbose_name='Numero carte VA scanné', blank=False, max_length=13, null=False)
    seems_legit = models.BooleanField(verbose_name="Semble légitime ?", default=True)
    check_place = models.ForeignKey("CheckPlace", null=True, on_delete=models.CASCADE, related_name="checks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.check_place.name + " - Student ID "+str(self.student_id)
