from django.contrib import admin

from .models import customUser, work

# Register your models here.
admin.site.register(customUser)
admin.site.register(work)