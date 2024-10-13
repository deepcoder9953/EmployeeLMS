from django.shortcuts import render, redirect
from .models import Empform, LeaveApplication, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import LeaveApplicationForm, EmpformRegistrationForm
from django.utils import timezone


def land(request):
    return render(request, 'land.html')

def register(request):
    if request.method == 'POST':
        form = EmpformRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('login') 
    else:
        form = EmpformRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = Empform.objects.filter(username=username, password=password)

        if user:
            request.session['username'] = username
            request.session['password'] = password  
          
            return redirect('/home')
        else:
            error = "Invalid credentials"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

def home(request):
    username = request.session.get('username')
    
    if username:
        approved_leaves = LeaveApplication.objects.filter(is_approved=True)

        total_leaves_taken = sum([leave.duration() for leave in approved_leaves])

        total_leaves_allowed = 30
        
        leaves_left = total_leaves_allowed - total_leaves_taken

        return render(request, 'home.html', {
            'username': username,
            'total_leaves_taken': total_leaves_taken,
            'leaves_left': leaves_left
        })
    else:
        return redirect('login')

def logout(request):
    return redirect('login')

def admin(request):
    return redirect('admin')

def dashboard(request):
    username = request.session.get('username') 
    
    if not username:
        return redirect('login')
     
    profile = Empform.objects.get(username=username)

    total_leave_limit = 30  
    current_year = timezone.now().year
    leaves_taken = LeaveApplication.objects.filter(
        start_date__year=current_year,
        is_approved=True,
    )

    total_leaves_taken = sum(leave.duration() for leave in leaves_taken)
    leaves_left = total_leave_limit - total_leaves_taken

    return render(request, 'dashboard.html', {
        'photo': profile.photo.url if profile.photo else None,
        'username': username,
        'full_name': f"{profile.firstname} {profile.lastname}",
        'position': profile.position,
        'address': profile.address,
        'total_leaves_taken': total_leaves_taken,
        'leaves_left': leaves_left,
    })

def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            print("success")
            leave_application = form.save(commit=False)
            leave_application.employee = request.user
            leave_application.save()
            return redirect('/leave-status')
    else:
        form = LeaveApplicationForm()
    
    return render(request, 'leave.html', {'form': form})

def leave_status(request):
    if request.user.is_authenticated:
        user = request.user
        leave_applications = LeaveApplication.objects.filter(employee=user)  
    else:
        leave_applications = []  
    context = {
        'leave_applications': leave_applications,
    }
    return render(request, 'leave_status.html', context)