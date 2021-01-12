from django.db import models
# import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime, timedelta
import calendar
from calendar import HTMLCalendar
from django.utils.translation import gettext as _
def current_time():
    return datetime.now()

def start_time():

    dt = datetime.now()
    start = dt - timedelta(days=dt.weekday())
    return  start

def end_time():
    dt = datetime.now()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return end
class PayrollProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='csmel')
    payrate = models.FloatField(blank=True, null=True, default=22.00)
    def __str__(self):
        return F"{self.payrate}"
class Payroll(models.Model):
    PAY_TYPE = (
        ('0', _('Regular')),
        ('1', _('EPL')),
        ('2', _('Vacation')),
        ('3', _('Sick')), )
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='csmel')
    payType = models.CharField( max_length=32,default='VAC', choices=PAY_TYPE
    )
    startTime = models.DateField(default=start_time)
    endTime = models.DateField(default=end_time)
    currentTime = models.DateField(default=current_time)
    monTime = models.FloatField(blank=True, null=True)
    tueTime = models.FloatField(blank=True, null=True)
    wedTime = models.FloatField(blank=True, null=True)
    thuTime = models.FloatField(blank=True,  null=True)
    friTime = models.FloatField(blank=True,  null=True)
    satTime = models.FloatField(blank=True,  null=True)
    sunTime = models.FloatField(blank=True,  null=True)
    totalTime = models.FloatField(blank=True, null=True)
    def __str__(self):
        return F"{self.user}: {self.startTime} - {self.endTime} // {self.payType}"
    def save(self, *args, **kwargs):
        self.totalTime = self.monTime + self.tueTime + self.wedTime + self.thuTime + self.friTime + self.satTime + self.sunTime
        return super(Payroll, self).save(*args, **kwargs)





class PayrollTotal(models.Model):
    identifier = models.IntegerField(unique=True, default=0)

    payroll_REG = models.ForeignKey(Payroll, blank=True, null=True, on_delete=models.CASCADE,related_name="payroll_REG", limit_choices_to={'payType': '0'},)
    paycode = models.CharField( max_length=32,default='Regular')
    rate = models.ForeignKey(PayrollProfile, blank=True, null=True, on_delete=models.SET_NULL,related_name="rate", default=3)
    total_reg_hours = models.FloatField(default=0.00)
    total_reg_hours_amount = models.FloatField(default=0.00)
    rate_overtime = models.FloatField(default=0.00)
    total_overtime_hours = models.FloatField(default=0.00)
    total_overtime_amount = models.FloatField(default=0.00)
    #EPL
    payroll_EPL = models.ForeignKey(Payroll, blank=True, null=True,  on_delete=models.SET_NULL,related_name="payroll_EPL", limit_choices_to={'payType': '1'},)
    start_bal_epl = models.FloatField(default=24)
    begin_bal_epl = models.FloatField(default=0.0)
    current_week_epl = models.FloatField(default=0.00)
    end_bal_epl = models.FloatField(default=0.00)
    #Vacation
    payroll_VAC = models.ForeignKey(Payroll,  blank=True, null=True, on_delete=models.SET_NULL,related_name="payroll_VAC", limit_choices_to={'payType': '2'},)
    start_bal_vac = models.FloatField(default=500)
    begin_bal_vac = models.FloatField(default=0.00)
    current_week_vac = models.FloatField(default=0.00)
    end_bal_vac = models.FloatField(default=0.00)
    #Sick
    payroll_SIC = models.ForeignKey(Payroll,  blank=True, null=True, on_delete=models.SET_NULL,related_name="payroll_SIC", limit_choices_to={'payType': '3'},)
    start_bal_sic = models.FloatField(default=500)
    begin_bal_sic = models.FloatField(default=0.00)
    current_week_sic = models.FloatField(default=0.00)
    end_bal_sic = models.FloatField(default=0.00)

    @receiver(post_save, sender=Payroll)
    def create_or_update_payroll_reg__payroll(sender,instance, created, **kwargs):
        if created:
            if instance.payType == '0':
                rate_instance = PayrollProfile.objects.get(user=33)
                PayrollTotal.objects.create(payroll_REG=instance, payroll_EPL=None, payroll_VAC=None, payroll_SIC=None, rate=rate_instance )

                print("Created")
            else:
                ori_REG = Payroll.objects.get(payType='0')
                if  Payroll.objects.filter(payType='1').exists():
                    ori_EPL = Payroll.objects.get(payType='1')
                else:
                    ori_EPL = None
                if Payroll.objects.filter(payType='2').exists():
                    ori_VAC = Payroll.objects.get(payType='2')
                else:
                    ori_VAC = None
                if Payroll.objects.filter(payType='3').exists():
                    ori_SIC = Payroll.objects.get(payType='3')
                else:
                    ori_SIC = None

                rate_instance = PayrollProfile.objects.get(user=33)

                PayrollTotal.objects.filter(identifier='0').update(payroll_REG=ori_REG, payroll_EPL=ori_EPL, payroll_VAC=ori_VAC , payroll_SIC=ori_SIC, rate=rate_instance )
                pt = PayrollTotal.objects.get(identifier='0', paycode='Regular')
                pt.save()
                print("Updated")

        else:
            print("Updated")

    def save(self, *args, **kwargs):
        if self.payroll_REG is not None:
            my_pay = self.payroll_REG
            my_pr = self.rate
            if my_pay.totalTime > 40:
                self.total_reg_hours = 40
                self.total_overtime_hours = my_pay.totalTime - 40 # overtime Hours
                self.total_overtime_amount = (my_pr.payrate * 1.5) * self.total_overtime_hours
                self.rate_overtime =  my_pr.payrate * 1.5
            elif my_pay.totalTime < 40:
                self.total_reg_hours = my_pay.totalTime
                self.total_overtime_hours = 0
                self.total_overtime_amount = 0
                self.rate_overtime =  0
            self.total_reg_hours_amount = self.total_reg_hours * my_pr.payrate


        #EPL
        if self.payroll_EPL is not None:
            my_pay_epl = self.payroll_EPL

            self.begin_bal_epl = 24
            self.current_week_epl = my_pay_epl.totalTime
            self.end_bal_epl = self.begin_bal_epl - self.current_week_epl
        elif self.payroll_EPL is None:
                self.current_week_epl = 0
                self.end_bal_epl = 0

        #VACATION
        if self.payroll_VAC is not None:
            my_pay_vac = self.payroll_VAC
            self.current_week_vac = my_pay_vac.totalTime
            self.end_bal_vac = self.begin_bal_vac - self.current_week_vac

        #VACATION
        if self.payroll_SIC is not None:
            my_pay_sic = self.payroll_SIC
            self.current_week_sic = my_pay_sic.totalTime
            self.end_bal_sic = self.begin_bal_sic - self.current_week_sic

        return super(PayrollTotal, self).save(*args, **kwargs)
