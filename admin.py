from django.contrib import admin

# Register your models here.
from .models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name','gender','department','speciality')
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','gender','idnumber','tel_num')
admin.site.register(Doctor,DoctorAdmin)