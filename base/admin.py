from django.contrib import admin

# Register your models here.

from .models import Job, Company

admin.site.register(Job)
admin.site.register(Company)