from django.shortcuts import render
from .models import Employee, Task
# Create your views here.
def home(request):
    return render(request, "home.html")

def login(request):
    employees = Employee.objects.all()
    return render(request, "login.html", {'employees': employees})

#The user route perhaps needs to take in an employee object of that specific user
#Need to find a way to pass in the employee information from the login screen.
def user(request):
    tasks = Task.objects.all()
    return render(request, "user.html", {'tasks': tasks})

def superuser(request):
    employees = Employee.objects.all()
    tasks = Task.objects.all()
    return render(request, "superuser.html", {'employees': employees, 'tasks': tasks})