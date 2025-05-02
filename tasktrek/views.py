from django.shortcuts import render
from .models import Employee, Task
import sqlite3


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


def handlelogin(request):
    founduser = False
    correctlogin = False
    adminflag = False
    dataConnector = sqlite3.connect('db.sqlite3')
    cursor = dataConnector.cursor()
    context = {}
    username = request.POST.get('login1', None)
    password = request.POST.get('login2', None)
    print("GETTING LOGIN INFORMATION")
    print(username)
    print(password)
    print(type(password))
    sql = "SELECT * FROM tasktrek_employee"
    cursor.execute(sql)
    employees = cursor.fetchall()
    #print(employees)

    for employee in employees:
        if username == employee[5]:
            founduser = True
            print("Found user!")
            print(employee)
            if employee[4] == int(password):
                correctlogin = True
                print("Password matches!!!")
                context['employee'] = employee
                if employee[2] == 1:
                    adminflag = True


    if not founduser:
        print("Invalid username or password")
        #Pass in error case to display error message in html
        return render(request, "login.html")

    if founduser and not correctlogin:
        print("Invalid password")
        return render(request, "login.html")

    #Get login information

    #Validate
    print(employee[2])
    print(type(employee[2]))
    #Check admin
    if adminflag:
        return render(request, "superuser.html", context)
    else:
        return render(request, "user.html", context)
    #Render appropriate view
    #return render(request, "test.html")
    