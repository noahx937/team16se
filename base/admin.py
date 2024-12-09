from django.contrib import admin

# Register your models here.

from .models import Job, Company, User

admin.site.register(Job)
admin.site.register(Company)
admin.site.register(User)