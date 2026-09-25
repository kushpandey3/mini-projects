import json
filepath = "tasks.json" #complete
#every task has a priority, isCompleted, and title
def recieveCommand():
    #display different types of tasks differently -> pandas?
    print("Which command would you like to use? \n")
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
    #validate input
    while invalid:
        try:
            command = int(input("Which command would you like to use? "))
            if command>=min and command <= max:
                invalid = False
            else:
                print(f"Please respond with a number between {min} and {max}")
        except ValueError:
            print(f"Please respond with a number between {min} and {max}")
    # is breaking necessary? test test
    match command:
        case 1:
            viewAllTasks()
        case 2:
            addTask()
        case 3:
            completeTask()
        case 4:
            deleteTask()
        case 5:
            searchForTask()
        case 6:
            viewCompletedTasks()
        case 7:
            viewUncompletedTasks()
        case 8:
            print(f"Thank you for using this task manager, {tasks[0]["Name"]}")
            return
    print("\n")
    recieveCommand()

            
def viewAllTasks():
    print(f"{tasks[0]["Name"]}'s Tasks \n")
    print(f"{"#":<10}{"Task":<50}{"Status":<12}{"Priority":<10}")
    for num in range(1, len(tasks)):
        print(f'{num:<10}{tasks[num]["Title"]:<50}{tasks[num]["Completed"]:<12}{tasks[num]["Priority"]:<10}')
    print()

def viewCompletedTasks():
    print(f"{tasks[0]["Name"]}'s Completed Tasks \n'")
    print(f"{"#":<10}{"Task":<50}{"Priority":<10}")
    for num in range(len(completed)):
         print(f'{num:<10}{completed[num]["Title"]:<50}{completed[num]["Priority"]:<10}')
    print()


def viewUncompletedTasks():
    print(f"{tasks[0]["Name"]}'s Completed Tasks \n'")
    print(f"{"#":<10}{"Task":<50}{"Priority":<10}")
    for num in range(len(completed)):
        print(f'{num:<10}{uncompleted[num]["Title"]:<50}{uncompleted[num]["Priority"]:<10}')
    print()
        
def addTask():
    title = input("Please enter the title of your task: ")
    invalid = True
    while invalid:
        try:
            priority = int(input("\n Please enter the priority of your task. Lower numbers signify higher priority. "))
            invalid = False
        except ValueError:
            print("Please enter an integer as your priority")
    l, r = 1, len(tasks)
    while l < r:
        mid = l + (r-l)//2
        if tasks[mid]["Priority"]<priority:
            l = mid + 1
        else:
            r = mid
    tasks.insert(l, {"Title": title, "Priority": priority, "Completed":False})
    save()
    l, r = 1, len(completed)
    while l < r:
        mid = l + (r-l)//2
        if completed[mid]["Priority"] < priority:
            l = mid + 1
        else:
            r = mid
    completed.insert(l, {"Title": title, "Priority": priority, "Completed":False})

def completeTask():
    title = input("Please enter the title of your task: ")
    for x in range(1, len(tasks)):
        if tasks[x]["Title"]==title:
            if tasks[x]["Completed"]:
                print("That task is already completed\n")
                return
            else:
                tasks[x]["Completed"] = True
                print("The task has succesfully been marked as completed\n")             
                return
    print("The task was not found\n")


def deleteTask():
    title = input("Please enter the title of your task: ")
    for x in range(1, len(tasks)):
        if tasks[x]["Title"]==title:
            tasks.pop(x)
            print("The task was succesfully deleted\n")
    print("The task was not found\n")


def searchForTask(): 
    title = input("Please enter the title of your task: ")
    for x in range(1, len(tasks)):
        if tasks[x]["Title"]==title:
            print("Task has been found! ")
            print(f'{tasks[x]["Title"]:<50}{tasks[x]["Completed"]:<12}{tasks[x]["Priority"]:<10}')
    print("The task was not found\n")

def save():
    with open (filepath, "w") as fp:
        json.dump(tasks, fp)

def initialize():
    print("Welcome to your task manager! \n")
    name = input("What would you like me to call you? ")
    print(f"\n Understood. Hello, {name}. ")
    global tasks, uncompleted, completed
    tasks, uncompleted, completed = [{"Name": name}], [], []

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
    except FileNotFoundError:
        initialize()

reinitialize()
recieveCommand()

#add delay of ~.2 seconds