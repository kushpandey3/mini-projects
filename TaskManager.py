import json, time
filepath = "tasks.json"
#every task has a priority, isCompleted, and title
def recieveCommand():
    time.sleep(.2)
    print("List of commands\n")
    print("1. View all tasks\n")
    print("2. Add task\n")
    print("3. Complete task\n")
    print("4. Delete task\n")
    print("5. Search for task\n")
    print("6. View completed tasks\n")
    print("7. View uncompleted tasks\n")
    print("8. Exit\n")
    min, max = 1, 8
    command, invalid = 0, True
    while invalid:
        try:
            command = int(input("Which command would you like to use? "))
            if command>=min and command <= max:
                invalid = False
            else:
                print(f"Please respond with a number between {min} and {max}")
        except ValueError:
            print(f"Please respond with a number between {min} and {max}")
    match command:
        case 1:
            print("\nYou have chosen to view your tasks\n")
            viewAllTasks()
        case 2:
            print("\nYou have chosen to add a task\n")
            addTask()
        case 3:
            print("\nYou have chosen to complete a task\n")
            completeTask()
        case 4:
            print("\nYou have chosen to delete a task\n")
            deleteTask()
        case 5:
            print("\nYou have chosen to search for a task\n")
            searchForTask()
        case 6:
            print("\nYou have chosen to view your completed tasks\n")
            viewCompletedTasks()
        case 7:
            print("\nYou have chosen to view your uncompleted tasks\n")
            viewUncompletedTasks()
        case 8:
            print(f"\nThank you for using this task manager, {tasks[0]["Name"]}")
            return
    invalid = True
    while(invalid):
        cont = input("\nWould you like to continue? (Y/N)")
        if len(cont) > 0 and (cont[0]=="Y" or cont[0]=='y'):
            recieveCommand()
            invalid = False
        elif len(cont) > 0 and (cont[0] == "N" or cont[0] == "n"):
            print(f"Thank you for using this service today, {tasks[0]["Name"]}")
            invalid = False
        else:
            print("Please respond with a Y or N.")

            
def viewAllTasks():
    print(f"{tasks[0]["Name"]}'s Tasks \n")
    print(f"{"#":<10}{"Task":<50}{"Status":<12}{"Priority":<10}")
    for num in range(1, len(tasks)):
        print(f'{num:<10}{tasks[num]["Title"]:<50}{tasks[num]["Completed"]:<12}{tasks[num]["Priority"]:<10}')
    print()

def viewCompletedTasks():
    print(f"{tasks[0]["Name"]}'s Completed Tasks \n")
    print(f"{"#":<10}{"Task":<50}{"Priority":<10}")
    for num in range(len(completed)):
         print(f'{num+1:<10}{completed[num]["Title"]:<50}{completed[num]["Priority"]:<10}')
    print()


def viewUncompletedTasks():
    print(f"{tasks[0]["Name"]}'s Completed Tasks \n")
    print(f"{"#":<10}{"Task":<50}{"Priority":<10}")
    for num in range(len(uncompleted)):
        print(f'{num+1:<10}{uncompleted[num]["Title"]:<50}{uncompleted[num]["Priority"]:<10}')
    print()
        
def addTask():
    title = input("Please enter the title of your task: ")
    invalid = True
    while invalid:
        try:
            priority = int(input("Please enter the priority of your task. Lower numbers signify higher priority. "))
            invalid = False
        except ValueError:
            print("Please enter an integer as your priority")
    nTask = {"Title": title, "Priority": priority, "Completed": False}
    insertTask(tasks, nTask, 0)
    insertTask(uncompleted, nTask)
    save()

def insertTask(li, task, l = 0):
    r = len(li)
    while l < r:
        mid = l + (r-l)//2
        if(task["Priority"]> li[mid]["Priority"]):
            l = mid + 1
        else:
            r = mid
    li.insert(l, task)

def completeTask():
    title = input("Please enter the title of your task: ")
    for x in range(1, len(tasks)):
        if tasks[x]["Title"]==title:
            if tasks[x]["Completed"]:
                print("That task is already completed\n")
                return
            else:
                uncompleted.remove(tasks[x])
                tasks[x]["Completed"] = True
                insertTask(completed, tasks[x])
                print("The task has succesfully been marked as completed\n")      
                return 
    print("The task was not found\n")
    save()


def deleteTask():
    title = input("Please enter the title of your task: ")
    task = None 
    for x in range(1, len(tasks) - 1):
        if tasks[x]["Title"] == title:
            task = tasks.pop(x)
            print("The task was succesfully deleted\n")
    if task is None:
        print("The task was not found\n")
    elif task["Completed"]:
        for x in range(1, len(completed) - 1):
            if completed[x] == task:
                completed.pop(x)
    else:
        for x in range(1, len(uncompleted) - 1):
            if uncompleted[x] == task:
                uncompleted.pop(x)
    save()

def searchForTask(): 
    title = input("Please enter the title of your task: ")
    for x in range(1, len(tasks)):
        if tasks[x]["Title"]==title:
            print("Task has been found! ")
            print(f'{tasks[x]["Title"]:<50}{tasks[x]["Completed"]:<12}{tasks[x]["Priority"]:<10}\n')
    print("The task was not found\n")

def save():
    with open (filepath, "w") as fp:
        json.dump(tasks, fp)

def initialize():
    print("Welcome to your task manager! \n")
    name = input("What would you like me to call you? ")
    print(f"\nUnderstood. Hello, {name}. \n")
    global tasks, uncompleted, completed
    tasks, uncompleted, completed = [{"Name": name}], [], []
    save()

def reinitialize():
    try:
        with open(filepath) as fp:
            global tasks, uncompleted, completed
            tasks, uncompleted, completed = json.load(fp), [], []
            for i in range(1, len(tasks)):
                if(tasks[i]["Completed"]):
                    completed.append(tasks[i])
                else:
                    uncompleted.append(tasks[i])
        print(f"Welcome back, {tasks[0]["Name"]}\n")
    except FileNotFoundError:
        initialize()

reinitialize()
recieveCommand()