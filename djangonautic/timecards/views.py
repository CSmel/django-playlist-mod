
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import CreateTimecard
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Payroll, PayrollTotal, PayrollProfile
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

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
    payrollTotal = PayrollTotal.objects.filter(identifier='2020-12-21')
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
            prev_total = request.POST.get("payroll_set-3-totalTime")
            ppt = PayrollProfile.objects.get(user=33)
            pptEPL = ppt.eplBank
            pptVAC = ppt.eplVac
            if timecard_formset.is_valid():
                if float(prev_total) > float(pptEPL):
                    html = "<html><body>Errors,You only have" +str(pptEPL)+" left in your bank Go back</body></html>"
                    return HttpResponse(html)
                else:
                    convert_start = request.POST.get('startVal')
                    timecard_formset.save()
                    return redirect('timecards:timecardview')


        for x in range(4):
            if 'add-model-'+str(x)  in request.POST:
                timecard_formset = PayrollFormset(request.POST, request.FILES,instance=user,)
                prev_total = request.POST.get("payroll_set-"+str(x)+"-totalTime")
                get_paytype = request.POST.get("payroll_set-"+str(x)+"-payType")
                ppt = PayrollProfile.objects.get(user=33)
                pptEPL = ppt.eplBank
                pptVAC = ppt.vacBank
                pptVAC = ppt.sicBank
                if timecard_formset.is_valid():
                    if get_paytype == '1':
                        if float(prev_total) > float(pptEPL):
                            html = "<html><body>Errors, EPL"+str(pptEPL)+" Go back</body></html>"
                            return HttpResponse(html)
                        else:
                            convert_start = request.POST.get('startVal')
                            timecard_formset.save()
                            return redirect('timecards:timecardview')
                    elif get_paytype == '2':
                        if float(prev_total) > float(pptVAC):
                            html = "<html><body>Errors,VACATION"+str(pptVAC)+" Go back</body></html>"
                            return HttpResponse(html)
                        else:
                            convert_start = request.POST.get('startVal')
                            timecard_formset.save()
                            return redirect('timecards:timecardview')
                    elif get_paytype == '3':
                        if float(prev_total) > float(pptSIC):
                            html = "<html><body>Errors,VACATION"+str(pptSIC)+" Go back</body></html>"
                            return HttpResponse(html)
                        else:
                            convert_start = request.POST.get('startVal')
                            timecard_formset.save()
                            return redirect('timecards:timecardview')
                    else:
                        convert_start = request.POST.get('startVal')
                        timecard_formset.save()
                        return redirect('timecards:timecardview')
            else:
                print('add', x)
        for x in range(4):
            if 'remove-model-'+str(x) in request.POST:
                print("Found",[x])
                remove_pay_type = request.POST.get("payroll_set-"+str(x)+"-payType")
                remove_startswith = request.POST.get("payroll_set-"+str(x)+"-startTime")
                prev_total = request.POST.get("payroll_set-"+str(x)+"-totalTime")

                update_total = PayrollProfile.objects.get(user=33)
                nt = float(prev_total) + update_total.eplBank
                print (remove_startswith)
                PayrollProfile.objects.filter(user=33).update(eplBank=nt)

                Payroll.objects.filter(startTime__startswith=remove_startswith, payType=remove_pay_type).delete()
                pt = PayrollTotal.objects.get(identifier=remove_startswith)
                pp = PayrollProfile.objects.get(user=33)

                pt.current_week_epl = 0
                pt.end_bal_epl = pp.eplBank
                pt.save()
                return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'payroll':payroll,'timecard_formset':timecard_formset})
            else:
                print("remove")

        if 'prevMonth' in request.POST:
            #day = datetime.strptime(request.POST.get('curr_t_input'), '%Y-%m-%d').strftime('%Y-%m-%d')

            day = request.POST.get('curr_t_input')
            dt = datetime.strptime(day, '%Y-%m-%d')-timedelta(days=7)
            start = dt - timedelta(days=dt.weekday())
            convert_start = datetime.strftime(start, '%Y-%m-%d')
            payroll = Payroll.objects.filter(startTime__startswith=convert_start, payType='0')
            try:
                Payroll.objects.get(startTime__startswith=convert_start, payType='0')
            except ObjectDoesNotExist:

                return HttpResponse("Not Here")
            timecard_formset = PayrollFormset(instance=user, queryset=Payroll.objects.filter(startTime__startswith=convert_start))
            payrollTotal = PayrollTotal.objects.filter(identifier=convert_start)
            # format date/day myheader
            sdate = start  # start date
            sevendays = []
            for i in range(7):
                days = sdate + timedelta(days=i)
                sevendays.append(days)

            return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'sevendays':sevendays,'payroll':payroll,'timecard_formset':timecard_formset,'start':convert_start})
        elif 'nextMonth' in request.POST:
            #day = datetime.strptime(request.POST.get('curr_t_input'), '%Y-%m-%d').strftime('%Y-%m-%d')
            day = request.POST.get('curr_t_input')
            dt = datetime.strptime(day, '%Y-%m-%d')+timedelta(days=7)
            start = dt - timedelta(days=dt.weekday())
            convert_start = datetime.strftime(start, '%Y-%m-%d')
            payroll = Payroll.objects.filter(startTime__startswith=convert_start, payType='0')
            timecard_formset = PayrollFormset(instance=user, queryset=Payroll.objects.filter(startTime__startswith=convert_start))
            payrollTotal = PayrollTotal.objects.filter(identifier=convert_start)

            # format date/day myheader
            sdate = start  # start date
            print("startdate",convert_start)
            sevendays = []
            for i in range(7):
                days = sdate + timedelta(days=i)
                sevendays.append(days)

            return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'day':day, 'start':start,'sevendays':sevendays,'payroll':payroll,'timecard_formset':timecard_formset,'start':start,'convert_start':convert_start})
        return render(request,'timecards/timecard_create.html',{'payrollTotal':payrollTotal,'sevendays':sevendays,'payroll':payroll,'timecard_formset':timecard_formset, 'mycalender': mycalender,'myheader': myheader,})
    else:
        raise PermissionDenied
