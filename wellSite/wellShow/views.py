from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext



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
def receive_record(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            rec_diff = float(body['distance'])
            rec_well = body['well']

            # 👇 only allow user's own wells
            well = Well.objects.get(well_id=rec_well)
            if (rec_diff > well.depth):
                return JsonResponse({'message': 'To deep for that well'})
            Record.objects.create(
                well_rec=well,
                diff=rec_diff
            )

            return JsonResponse({'message': 'Success'})

        except Well.DoesNotExist:
            return JsonResponse({'message': 'No such well for this user'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'POST required'})

# ➕ Create new well

@csrf_exempt
@login_required
def create_well(request):
    print("create")
    if request.method == 'POST':
        try:
            #request_context = RequestContext(request)
            depth = float(request.POST.get('depth', 0))
            name = request.POST.get('name')

            well = Well.objects.create(
                name = name,
                depth=depth,
                user=request.user   # 👈 IMPORTANT
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
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('home')
        except:
            return render(request, 'signup.html', {'error': 'User already exists'})

    return render(request, 'signup.html')