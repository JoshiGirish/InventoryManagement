from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.models import EventCard

def display_history_view(request):
    if request.method == 'GET':
        events = EventCard.objects.all().order_by('-date')
        dictionaries = []
        for event in events: 
            dictionaries.append(event.__dict__)
        return render(request, 'history/history.html',{'dicts': dictionaries})