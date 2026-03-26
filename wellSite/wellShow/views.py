from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Well, Record


# 📊 Show graph
def home(request):
    wells = Well.objects.all().order_by('created_at')

    labels = [w.created_at.strftime("%H:%M:%S") for w in wells]
    data = [w.depth for w in wells]

    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }
    return render(request, 'home.html', context)


# 📥 Receive record (JSON POST)
@csrf_exempt
def receive_record(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            rec_diff = float(body['distance'])
            rec_well = body['well']

            well = Well.objects.get(well_id=rec_well)

            Record.objects.create(
                well_rec=well,
                diff=rec_diff
            )

            return JsonResponse({'message': 'Success'})

        except Well.DoesNotExist:
            return JsonResponse({'message': 'No such well'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'POST required'})


# ➕ Create new well
def create_well(request):
    if request.method == 'POST':
        try:
            depth = float(request.POST.get('depth', 0))

            well = Well.objects.create(depth=depth)

            return JsonResponse({
                'status': 'success',
                'well_id': str(well.well_id)
            })

        except Exception as e:
            return JsonResponse({'status': 'fail', 'reason': str(e)})

    return JsonResponse({'status': 'fail', 'reason': 'POST required'})