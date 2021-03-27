from django.shortcuts import render, get_object_or_404
from .models import Bear, Sighting

def bear_list(request):
    bears = Bear.objects.all()
    left_ear = 0
    right_ear= 0
    male = 0
    female = 0

    for bear in bears:
        if bear.sex == 'M':
            male += 1
        else:
            female += 1
        if  bear.ear_applied == 'Left':
            left_ear += 1
        else:
            right_ear += 1
        
    return render(request, 'bears/bear_list.html', {'bears' : bears, 
    'left_ear': left_ear, 'right_ear': right_ear, 'male': male, 'female': female})

def bear_detail(request, id):
    bear = get_object_or_404(Bear, id=id)
    sightings = Sighting.objects.filter(bear_id=id)
    return render(request, 'bears/bear_detail.html', {'bear' : bear, 'sightings' : sightings})