from django.contrib import admin
from .models import Empform, LeaveApplication
# Register your models here.

admin.site.register(Empform)

class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'is_approved']
    list_filter = ['is_approved', 'leave_type']

admin.site.register(LeaveApplication, LeaveApplicationAdmin)