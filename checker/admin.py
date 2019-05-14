from django.contrib import admin

# Register your models here.
from .models import *


# Register your models here.
@admin.register(CheckPlace, Screen)
class Admin(admin.ModelAdmin):
    pass

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = '__str__', 'seems_legit', 'check_place', 'created_at'
    list_display_links = '__str__',
    search_fields = 'student_id', 'created_at'
    list_filter = 'check_place', 'seems_legit'
