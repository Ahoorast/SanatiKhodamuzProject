from django.contrib import admin

from .models import customUser, work, jobAssignments

# Register your models here.
admin.site.register(customUser)
admin.site.register(work)
admin.site.register(jobAssignments)