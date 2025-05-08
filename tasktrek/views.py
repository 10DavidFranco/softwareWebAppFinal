from django.shortcuts import render, redirect
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
def user(request, employee_id):
    dataConnector = sqlite3.connect('db.sqlite3')
    cursor = dataConnector.cursor()
    print("Look at my employee id")
    print(employee_id)
    #Now look them up and get their info
    cursor.execute("SELECT * FROM tasktrek_employee WHERE id = ?", [employee_id])
    employee_data = cursor.fetchone()
    print("Look at my employee data")
    print(employee_data)

    employee_tasks = employee_data[3]
    print("Look at my employees tasks...")
    print(employee_tasks)
    print(type(employee_tasks))

    clean_employee_tasks = employee_tasks.split(",")
    print("Look at my REAL employee tasks...")
    print(clean_employee_tasks)

    task_list = Task.objects.all()
    clean_task_list = []

    

    for task in task_list:
        copy_task = str(task)
        clean_task_list.append(copy_task.split("~"))

    print("Cleaned up task list")
    print(clean_task_list)


    #IF task id matches, store it in task array to be passed into template
    #For every task id a user has, get the appropriate task
    task_array = []
    for a_task_id in clean_employee_tasks:
        for a_task in clean_task_list:
            if a_task_id == a_task[0]:
                task_array.append(Task.objects.get(id=a_task_id))

    print("All tasks compiled!!!")
    print(type(task_array[0]))
    #We still need to handle edge cases...but its a start



    #Need to find employee tasks from task_list and send them to template in variable calld tasks

    context = {
        'tasks' : task_array,
        'name' : employee_data[1]
    }
    return render(request, "user.html", context)

def superuser(request, employee_id):
    dataConnector = sqlite3.connect('db.sqlite3')
    cursor = dataConnector.cursor()
    print("Woah look at Mr big shot over here")
    print(employee_id)
    employees = Employee.objects.all()
    tasks = Task.objects.all()



    print("Look at my employees...")
    print(employees)

    clean_employee_list = []
    for employee in employees:
        clean_copy = str(employee)
        clean_employee_list.append(clean_copy.split("~"))
    print(clean_employee_list)
    #Need to clean the task list for searching

    for employee in clean_employee_list:
        clean_task_list = employee[3].split(",")
        task_words = []
        for task_id in clean_task_list:
            #IF WE ASSIGN GROUP TASKS WE NEED TO KEEP THIS CHECK IN MIND....I AM CHECKING FOR TEXT NOT BOOL , MAYBVE DELETE DUMMY TASKS
            cursor.execute("SELECT name FROM tasktrek_task WHERE id = ? AND is_team = ?", [task_id, "False"])
            task_words.append(cursor.fetchone()[0])
            print(task_id)
        print("Look at my task words")
        print(task_words)
        employee[3] = task_words
            
    print("Finally my list is made!!!")
    print(clean_employee_list)

    new_employee_list = []
    for employee in clean_employee_list:
        new_employee = {
            'id': employee[0],
            'name': employee[1],
            'is_admin': employee[2],
            'tasks': employee[3],
            'username': employee[4],
            'password': employee[5]
        }

        new_employee_list.append(new_employee)

    print("NOWWWW it's done...")
    print(new_employee_list)
    
    cursor.execute("SELECT name FROM tasktrek_task WHERE is_team = ?", ["True"])
    group_tasks = cursor.fetchall()
    print("Look at my group tasks")
    #print(len(group_tasks))
    print(type(group_tasks))


    clean_group_tasks = []
    for group_task in group_tasks:
        print(type(group_task))
        group_task_copy = str(group_task)
        print(group_task_copy)
        good_copy = group_task_copy[2:len(group_task_copy)-3]
        print(good_copy)
        clean_group_tasks.append(good_copy)
    print(clean_group_tasks)

    #Need to go into the task_list of each employee and replace it with a list of task_names/titles
    #or we can do this on the html page...
    # for task in tasks, no because an employee is only iterated through once, we want the titles in a list all ready to go for display
    return render(request, "superuser.html", {'employees': new_employee_list, 'group_tasks': clean_group_tasks})


def handlelogin(request):
    founduser = False
    correctlogin = False
    adminflag = False
    dataConnector = sqlite3.connect('db.sqlite3')
    cursor = dataConnector.cursor()
    #context = {}
    username = request.POST.get('login1', None)
    password = request.POST.get('login2', None)
    print("GETTING LOGIN INFORMATION")
    print(username)
    print(password)
    print(type(password))
    sql = "SELECT * FROM tasktrek_employee"
    cursor.execute(sql)
    employees = cursor.fetchall()
    employee_id = None
    #print(employees)

    for employee in employees:
        if username == employee[5]:
            founduser = True
            print("Found user!")
            print(employee)
            if employee[4] == int(password):
                correctlogin = True
                employee_id = employee[0]
                print("Password matches!!!")
                #my_employee = employee
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
        return redirect("superuser", employee_id = employee_id)
    else:
        #Need to pass in name and tasks
        return redirect("user", employee_id= employee_id)
    #Render appropriate view
    #return render(request, "test.html")
    