
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import CreateTimecard
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Payroll, PayrollTotal
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django import forms

import calendar
from calendar import HTMLCalendar
from django.forms.models import inlineformset_factory
# Create your views here.
def timecards_view(request):

    return render(request,'timecards/timecard_view.html')

def timecard_create(request, pk):

    sdate = date(2020, 12, 21)   # start date
    edate = date(2008, 9, 15)   # end date
    sevendays = []
    for i in range(7):
        days = sdate + timedelta(days=i)
        sevendays.append(days)
    payroll = Payroll.objects.filter(startTime__startswith='2020-12-21', payType='0')
    payrollTotal = PayrollTotal.objects.all()
    themonth = 12
    theyear = 2020
    mycalender =  calendar.monthcalendar(theyear, themonth)
    myheader = calendar.weekheader(3)
    user = User.objects.get(pk=pk)
    PayrollFormset = inlineformset_factory(User, Payroll, extra=1, fields=('startTime','payType','user','sunTime','monTime','tueTime','wedTime','thuTime','friTime','satTime','totalTime' ),
    widgets={
        'payType': forms.Select( attrs={ 'class': 'form-control selectpicker'} ),
    'sunTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'monTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'tueTime': forms.TextInput( attrs={ 'class': 'form-control date', 'placeholder': 'Title',"data-date-format": "dd.mm.yyyy" } ),
    'wedTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'thuTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'friTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'satTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'totalTime': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    })
    timecard_formset = PayrollFormset(instance=user, queryset=Payroll.objects.filter(startTime__startswith='2020-12-21'))
    if request.user.is_authenticated and request.user.id == user.id:
        if 'timesheetBtn' in request.POST:
            timecard_formset = PayrollFormset(request.POST, request.FILES,instance=user,)
            if timecard_formset.is_valid():
                convert_start = request.POST.get('startVal')
                timecard_formset.save()
                return redirect('timecards:timecardview')
        elif 'add-model-0' in request.POST:
            timecard_formset = PayrollFormset(request.POST, request.FILES,instance=user,)
            if timecard_formset.is_valid():
                convert_start = request.POST.get('startVal')
                timecard_formset.save()
                return redirect('timecards:timecardview')
        elif 'add-model-1' in request.POST:
            timecard_formset = PayrollFormset(request.POST, request.FILES,instance=user,)
            if timecard_formset.is_valid():
                convert_start = request.POST.get('startVal')
                timecard_formset.save()
                return redirect('timecards:timecardview')
        elif 'add-model-2' in request.POST:
            timecard_formset = PayrollFormset(request.POST, request.FILES,instance=user,)
            if timecard_formset.is_valid():
                convert_start = request.POST.get('startVal')
                timecard_formset.save()
                return redirect('timecards:timecardview')
        elif 'remove-model-0' in request.POST:
             remove_pay_type = request.POST.get('payroll_set-0-payType')
             remove_startswith = request.POST.get('payroll_set-0-startTime')
             print (remove_startswith)
             Payroll.objects.filter(startTime__startswith=remove_startswith, payType=remove_pay_type).delete()
             return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'payroll':payroll,'timecard_formset':timecard_formset})
        elif 'remove-model-1' in request.POST:
             remove_pay_type = request.POST.get('payroll_set-1-payType')
             remove_startswith = request.POST.get('payroll_set-1-startTime')
             print (remove_startswith)
             Payroll.objects.filter(startTime__startswith=remove_startswith, payType=remove_pay_type).delete()
             return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'payroll':payroll,'timecard_formset':timecard_formset})
        elif 'remove-model-2' in request.POST:
             remove_pay_type = request.POST.get('payroll_set-2-payType')
             remove_startswith = request.POST.get('payroll_set-2-startTime')
             print (remove_startswith)
             Payroll.objects.filter(startTime__startswith=remove_startswith, payType=remove_pay_type).delete()
             return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'payroll':payroll,'timecard_formset':timecard_formset})
        elif 'remove-model-3' in request.POST:
             remove_pay_type = request.POST.get('payroll_set-3-payType')
             remove_startswith = request.POST.get('payroll_set-3-startTime')
             print (remove_startswith)
             Payroll.objects.filter(startTime__startswith=remove_startswith, payType=remove_pay_type).delete()
             return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'payroll':payroll,'timecard_formset':timecard_formset})
        elif 'prevMonth' in request.POST:
            #day = datetime.strptime(request.POST.get('curr_t_input'), '%Y-%m-%d').strftime('%Y-%m-%d')

            day = request.POST.get('curr_t_input')
            dt = datetime.strptime(day, '%Y-%m-%d')-timedelta(days=6)
            start = dt - timedelta(days=dt.weekday())
            convert_start = datetime.strftime(start, '%Y-%m-%d')
            payroll = Payroll.objects.filter(startTime__startswith=convert_start)
            timecard_formset = PayrollFormset(instance=user, queryset=Payroll.objects.filter(startTime__startswith=convert_start))

            # format date/day myheader
            sdate = start  # start date
            sevendays = []
            for i in range(7):
                days = sdate + timedelta(days=i)
                sevendays.append(days)

            return render(request,'timecards/timecard_create.html',{'sevendays':sevendays,'payroll':payroll,'timecard_formset':timecard_formset,'start':convert_start})
        elif 'nextMonth' in request.POST:
            #day = datetime.strptime(request.POST.get('curr_t_input'), '%Y-%m-%d').strftime('%Y-%m-%d')
            day = request.POST.get('curr_t_input')
            dt = datetime.strptime(day, '%Y-%m-%d')+timedelta(days=6)
            start = dt - timedelta(days=dt.weekday())
            convert_start = datetime.strftime(start, '%Y-%m-%d')
            payroll = Payroll.objects.filter(startTime__startswith=convert_start)
            timecard_formset = PayrollFormset(instance=user, queryset=Payroll.objects.filter(startTime__startswith=convert_start))
            # format date/day myheader
            sdate = start  # start date
            sevendays = []
            for i in range(7):
                days = sdate + timedelta(days=i)
                sevendays.append(days)

            return render(request,'timecards/timecard_create.html',{'sevendays':sevendays,'payroll':payroll,'timecard_formset':timecard_formset,'start':convert_start})
        return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'sevendays':sevendays,'payroll':payroll,'timecard_formset':timecard_formset, 'mycalender': mycalender,'myheader': myheader,})
    else:
        raise PermissionDenied
