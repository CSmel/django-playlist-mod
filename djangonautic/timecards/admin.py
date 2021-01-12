from django.contrib import admin

# Register your models here.
from .models import Payroll, PayrollTotal, PayrollProfile
# admin.site.register(Payrollusr)
class PayrollAdmin(admin.ModelAdmin):
    list_filter = ('user','startTime')
    list_display = ('user','startTime', 'endTime','payType')
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(PayrollTotal)
admin.site.register(PayrollProfile)
