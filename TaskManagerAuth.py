import hashlib
import json
import os

# File paths
USERS_FILE = "D:\\IITM\\IITM AG\\Python Fundamentals\\Python_Project\\Proj2\\users.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, 'w').close()

    with open(USERS_FILE, 'r') as file:
        users = file.readlines()

    for user in users:
        if user.split(':')[0] == username:
            print("Username already exists.")
            return False

    with open(USERS_FILE, 'a') as file:
        file.write(f"{username}:{hash_password(password)}\n")
    print("Registration successful!")
    return True

def login_user(username, password):
    with open(USERS_FILE, 'r') as file:
        users = file.readlines()

    for user in users:
        stored_username, stored_password = user.strip().split(':')
        if stored_username == username and stored_password == hash_password(password):
            print("Login successful!")
            return True

    print("Invalid username or password.")
    return False

def get_tasks_file(username):
    return f"D:\\IITM\\IITM AG\\Python Fundamentals\\Python_Project\\Proj2\\tasks_{username}.txt"

def add_task(username, title, description):
    tasks_file = get_tasks_file(username)
    tasks = []

    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as file:
            tasks = json.load(file)

    task = {"id": len(tasks) + 1, "title": title, "description": description, "completed": False}
    tasks.append(task)

    with open(tasks_file, 'w') as file:
        json.dump(tasks, file, indent=4)

    print("Task added successfully!")

def view_tasks(username):
    tasks_file = get_tasks_file(username)

    if not os.path.exists(tasks_file):
        print("No tasks found.")
        return

    with open(tasks_file, 'r') as file:
        tasks = json.load(file)

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Completed" if task['completed'] else "Pending"
        print(f"[ID: {task['id']}] {task['title']} - {task['description']} ({status})")

def mark_task_completed(username, task_id):
    tasks_file = get_tasks_file(username)

    if not os.path.exists(tasks_file):
        print("No tasks found.")
        return

    with open(tasks_file, 'r') as file:
        tasks = json.load(file)

    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            with open(tasks_file, 'w') as file:
                json.dump(tasks, file, indent=4)
            print("Task marked as completed!")
            return

    print("Task ID not found.")

def delete_task(username, task_id):
    tasks_file = get_tasks_file(username)

    if not os.path.exists(tasks_file):
        print("No tasks found.")
        return

    with open(tasks_file, 'r') as file:
        tasks = json.load(file)

    tasks = [task for task in tasks if task['id'] != task_id]

    with open(tasks_file, 'w') as file:
        json.dump(tasks, file, indent=4)

    print("Task deleted successfully!")

def main():
    while True:
        print("\n--- Task Manager ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_user(username, password):
                while True:
                    print("\n--- Task Menu ---")
                    print("1. Add Task")
                    print("2. View Tasks")
                    print("3. Mark Task as Completed")
                    print("4. Delete Task")
                    print("5. Logout")
                    task_choice = input("Enter your choice: ")

                    if task_choice == '1':
                        title = input("Enter task title: ")
                        description = input("Enter task description: ")
                        add_task(username, title, description)

                    elif task_choice == '2':
                        view_tasks(username)

                    elif task_choice == '3':
                        task_id = int(input("Enter task ID to mark as completed: "))
                        mark_task_completed(username, task_id)

                    elif task_choice == '4':
                        task_id = int(input("Enter task ID to delete: "))
                        delete_task(username, task_id)

                    elif task_choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again.")

        elif choice == '3':
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
