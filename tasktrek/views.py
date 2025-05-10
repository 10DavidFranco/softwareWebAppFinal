from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Employee, Task
import sqlite3
import json


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

    cursor.execute("SELECT * FROM tasktrek_task WHERE is_team = ?", ["True"])
    group_tasks = cursor.fetchall()
    print("Look at my group tasks")
    print(group_tasks)
    print(type(group_tasks))


    clean_group_tasks = []
    
    for group_task in group_tasks:
        gt_entry = {}
        print(type(group_task))
        gt_entry['id'] = group_task[0]
        gt_entry['name'] = group_task[3]
        gt_entry['description'] = group_task[1]
        gt_entry['due_date'] = group_task[2]
        clean_group_tasks.append(gt_entry)
        
    print(clean_group_tasks)



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
    if employee_tasks != "":
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
            'name' : employee_data[1],
            'group_tasks': clean_group_tasks
        }
        return render(request, "user.html", context)
    else:
        context = {
            'tasks' : "",
            'name' : employee_data[1],
            'group_tasks': clean_group_tasks
            
        }
        return render(request, "user.html", context)

def superuser(request, employee_id):
    dataConnector = sqlite3.connect('db.sqlite3')
    cursor = dataConnector.cursor()



    print("Woah look at Mr big shot over here")
    print(employee_id)
    print(type(employee_id))
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
    #Make an array of dictionaries, each index will have a dictionary with id and desc
    for employee in clean_employee_list:
        if(employee[3] == ""):
            continue
        else:
            clean_task_list = employee[3].split(",")
            task_list = []
            for task_id in clean_task_list:
                #IF WE ASSIGN GROUP TASKS WE NEED TO KEEP THIS CHECK IN MIND....I AM CHECKING FOR TEXT NOT BOOL , MAYBVE DELETE DUMMY TASKS
                cursor.execute("SELECT name FROM tasktrek_task WHERE id = ? AND is_team = ?", [task_id, "False"])
                task_entry = {}
                task_entry['id'] = task_id
                task_entry['description'] = cursor.fetchone()[0]
                cursor.execute("SELECT is_complete FROM tasktrek_task WHERE id = ? AND is_team = ?", [task_id, "False"])
                task_entry['is_complete'] = cursor.fetchone()[0]
                task_list.append(task_entry)
                print(task_id)
            print("Look at my task list")
            print(task_list)
            employee[3] = task_list
            
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
    
    cursor.execute("SELECT * FROM tasktrek_task WHERE is_team = ?", ["True"])
    group_tasks = cursor.fetchall()
    print("///////////////////////////////////////////////////")
    print("Look at my group tasks")
    #print(len(group_tasks))
    print(group_tasks)
    #We need to pass in the id's of the group tasks so the edit button can work...

    clean_group_tasks = []
    for group_task in group_tasks:
        gt_entry = {}
        gt_entry['id'] = group_task[0]
        gt_entry['title'] = group_task[3]
        gt_entry['description'] = group_task[1]
        gt_entry['due_date'] = group_task[2]
        
        print("ASSEMBLED GT ENTRY")
        print(gt_entry)
        print("$$$$$$$$$$")
        clean_group_tasks.append(gt_entry)
    print(clean_group_tasks)

    #Need to go into the task_list of each employee and replace it with a list of task_names/titles
    #or we can do this on the html page...
    # for task in tasks, no because an employee is only iterated through once, we want the titles in a list all ready to go for display
    return render(request, "superuser.html", {'employees': new_employee_list, 'group_tasks': clean_group_tasks, 'admin_id': employee_id})


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


def handledelete(request, admin_id, employee_id, task_id):
    print("Handling delete")
    print("Id of admin")
    print(admin_id)
    print("Employee id")
    print(employee_id)
    print("Task id")
    print(task_id)
    print(type(task_id))
    #Need to adjust employee building to include taskids so that they can be used here!
    #Need to rerender superuser view!!!! Which means we need to find a way to pass the admin id to this function!!!


    #Get employee task list
    dataConnector = sqlite3.connect('db.sqlite3')
    cursor = dataConnector.cursor()
    print("Look at my employee id")
    print(employee_id)
    #Now look them up and get their info
    employees = Employee.objects.all()
    my_employee = None
    for employee in employees:
        if employee.id == employee_id:
            my_employee = employee
    print("Look at my employee data")
    print(my_employee)

    employee_tasks = my_employee.tasks
    print("Look at my employees tasks...")
    print(employee_tasks)
    print(type(employee_tasks))

    clean_employee_tasks = employee_tasks.split(",")
    print("Look at my REAL employee tasks...")
    print(clean_employee_tasks)
    #Find task with matching id
    new_tasks = []
    for task in clean_employee_tasks:
        if task == str(task_id):
            print("Found the task to remove:")
            print(task)
        else:
            print("Not you")
            new_tasks.append(task)
    #Remove and reassign
    print("Look at my new tasks:")
    print(new_tasks)
    #Make into string text and push to db
    string_tasks = ','.join(new_tasks)
    print("Made into string")
    print(string_tasks)



    #The real meat and potatoes
    employee = Employee.objects.get(id=employee_id)
    employee.tasks = string_tasks
    employee.save()
    #Rerender
    #return HttpResponse("Ok", status=200)


    #Perhaps becuase we have a blank argument, they are being positionally shifted over 1?
    return redirect("superuser", employee_id = admin_id)



def handlecreate(request, admin_id):
    print("Creating new task!")
    selected_employee = request.POST.get('employee_id')


    #Get the employee!!!
    print("Look at the employee they chose")
    print(selected_employee)

    #Now get the info to create the task
    title = request.POST.get('task_title')
    date = request.POST.get('due_date')
    t_type = request.POST.get('task_type')
    description = request.POST.get('task_description')
    print("Look what they sent me...")
    print(title)
    print(date)
    print(t_type)
    print(description)

    is_team = None
    if(t_type == "individual"):
        is_team = "False"
        #Now create the task!!!
        new_task = Task.objects.create(name= title, description= description, due_date=date, is_complete="False", is_team=is_team)
        


        #Now update the employee and save
        employee = Employee.objects.get(id=selected_employee)
        print("Alright lets check out what tasks this employee currently has...")
        print(employee.tasks)
        current_tasks = employee.tasks
        print(type(current_tasks))
        
        print("This is the id of the new task")
        print(new_task.id)
        new_entry = new_task.id

        if(current_tasks == ""):
            employee.tasks = new_entry
        else:
            employee.tasks = current_tasks + "," + str(new_entry)

        employee.save()


        #Lastly rerender
        #return HttpResponse("Ok", status=200)
        return redirect("superuser", employee_id = admin_id)
    else:
        is_team = "True"
        new_task = Task.objects.create(name= title, description= description, due_date=date, is_complete="False", is_team=is_team)
        new_task.save()
        
        #Wait group tasks dont need to be assigned to people, they jsut need to be created in the databse
        
        return redirect("superuser", employee_id = admin_id)
    

def handleedit(request):
    print("Handling edit")
    print("Lets take a peek at the request...")
    print(request)
    data = json.loads(request.body)
    print("What about data?")
    print(data.get('data'))
    #I need to pass in the id...all the way here from the html-> js -> python
    new_title = data.get('title')
    new_description = data.get('desc')
    admin_id = data.get('admin_id')
    task_id = data.get('task_id')

    print("Alright lets check our stuff")
    print(new_title)
    print(new_description)
    print(admin_id)
    print(task_id)

    #Look up Task objects based on id
    task_to_change = Task.objects.get(id=task_id)
    
    #Update fields
    task_to_change.name = new_title
    task_to_change.description = new_description
    task_to_change.save()
    #Render admin view? Which would also require passing in the adminid...

    return HttpResponse("Ok", status=200)

def handlecomplete(request):
    print("Handling completion")
    data = json.loads(request.body)
    task_id = data.get('task_id')
    completed = data.get('completion')
    print("Task to be changed...")
    print(task_id)
    print("So it's done?")
    print(completed)
    


    #Find task based on id and set is_complete to true...
    task_to_complete = Task.objects.get(id=task_id)
    
    #Update fields
    task_to_complete.is_complete = completed
    
    task_to_complete.save()

    #We will just have to make it where no one has the same two individual tasks
    return HttpResponse("Ok", status=200)