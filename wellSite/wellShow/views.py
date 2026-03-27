from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from datetime import timedelta
from django.views.decorators.http import require_POST


def logout_view(request):
    logout(request)
    return redirect('/')

# 📊 Show graph
#@login_required
@login_required
def home(request):
    wells = Well.objects.filter(user=request.user).order_by('created_at')

    selected_well_id = request.GET.get('well')
    selected_well = None

    if selected_well_id:
        try:
            selected_well = wells.get(well_id=selected_well_id)
        except Well.DoesNotExist:
            selected_well = None

    # ✅ If a well is selected → ONLY its records
    if selected_well:
        records = Record.objects.filter(
            well_rec=selected_well
        ).order_by('created_at')

    else:
        # ✅ If no well selected → all records
        records = Record.objects.filter(
            well_rec__user=request.user
        ).order_by('created_at')

    # ✅ Always build from records (even if empty)
    labels = [r.created_at.strftime("%H:%M:%S") for r in records]
    data = [r.diff for r in records]

    context = {
        'wells': wells,
        'selected_well': selected_well,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }

    return render(request, 'home.html', context)
# 📥 Receive record (JSON POST)
#@login_required
@csrf_exempt
@login_required


def inbox(request):
    events = Event.objects.order_by('-created_at')[:50]

    grouped = []
    TIME_WINDOW = timedelta(minutes=5)

    for event in events:
        if not grouped:
            grouped.append({
                "event": event,
                "count": 1
            })
            continue

        last_event = grouped[-1]["event"]

        same_source = event.well_id_value == last_event.well_id_value
        close_in_time = abs(event.created_at - last_event.created_at) <= TIME_WINDOW
        same_type = event.event_type == last_event.event_type
        same_message = event.message == last_event.message

        if same_source and close_in_time and same_type and same_message:
            grouped[-1]["count"] += 1
        else:
            grouped.append({
                "event": event,
                "count": 1
            })

    return render(request, 'inbox.html', {
        'events': grouped
    })

@require_POST
@login_required
def resolve_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.resolved = True
    event.save()
    return redirect('inbox')


@require_POST
@login_required
def create_well_from_event(request, event_id):
    event = Event.objects.get(id=event_id)

    name = request.POST.get('name')
    depth = request.POST.get('depth')
    radius = request.POST.get('radius')

    if event.well_id_value:
        Well.objects.get_or_create(
            well_id=event.well_id_value,
            defaults={
                'name': name,
                'depth': float(depth),
                'radius': float(radius),  # ✅ NEW
                'user': request.user
            }
        )

    event.resolved = True
    event.save()

    return redirect('inbox')

@csrf_exempt
def receive_record(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            rec_diff = float(body.get('distance'))
            rec_well = int(body.get('well'))

            try:
                # ✅ Try to find the well
                well = Well.objects.get(well_id=rec_well)

            except Well.DoesNotExist:
                # 🔴 Log event instead of creating well
                Event.objects.create(
                    event_type='warning',
                    message=f"Unknown well ID received: {rec_well}",
                    well_id_value=rec_well
                )

                return JsonResponse({
                    'status': 'unknown_well',
                    'well_id': rec_well
                })

            # ✅ Save record if well exists
            # Convert sensor distance → water height
            water_height = well.depth - rec_diff

            Record.objects.create(
                well_rec=well,
                diff=water_height
            )

            return JsonResponse({
                'status': 'ok',
                'well_id': rec_well
            })

        except Exception as e:
            # 🔴 Log unexpected errors
            Event.objects.create(
                event_type='error',
                message=str(e)
            )

            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({'status': 'POST required'})
# ➕ Create new well

@csrf_exempt
@login_required
def create_well(request):
    print("create")
    if request.method == 'POST':
        try:
            #request_context = RequestContext(request)
            depth = float(request.POST.get('depth', 0))
            radius = float(request.POST.get('radius', 0))  # ✅ NEW
            name = request.POST.get('name')

            well = Well.objects.create(
            name=name,
            depth=depth,
            radius=radius,  # ✅ NEW
            user=request.user
)
            print(well.well_id)

            return redirect('home')

        except Exception as e:
            print(str(e))
            return JsonResponse({'status': 'fail', 'reason': str(e)})

    return JsonResponse({'status': 'fail', 'reason': 'POST required'})

def start(request):
    return render(request, 'starter_page.html')


# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# SIGN UP
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.create_user(username=username, password=password)
            user = User.objects.get(username='arduino')
            login(request, user)
            return redirect('home')
        except:
            return render(request, 'signup.html', {'error': 'User already exists'})

    return render(request, 'signup.html')