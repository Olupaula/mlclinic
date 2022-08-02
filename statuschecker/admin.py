from django.contrib import admin
from .models import Doctor, Patient, BreastCancer, Diabetics

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(BreastCancer)
admin.site.register(Diabetics)

