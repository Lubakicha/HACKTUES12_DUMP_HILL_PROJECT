from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *

# Create your views here.

##################################################
# (Recieve)

@csrf_exempt
def new_rec(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        # Use request.POST for form data or request.body for JSON data
        rec_diff = body['distance']
        rec_well = body['well']
        try: 
            well = Well.objects.get(well_id = rec_well)
            rec = Record(well_rec = well, diff = rec_diff)
            rec.save()
            return JsonResponse({'message':'Success'})
        except: return JsonResponse({'message': 'No such well'})
    return JsonResponse({'message':'Gotta be POST'})

#@csrf_exempt
#def new_well(request):

##################################################
# (Show)

def home(request):
    print('home')
    template = loader.get_template('home.html')
    return HttpResponse(template.render())