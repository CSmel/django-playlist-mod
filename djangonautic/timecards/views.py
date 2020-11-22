from django.shortcuts import render
# Create your views here.
def timecards_view(request):

    return render(request,'timecards/timecard_view.html')
