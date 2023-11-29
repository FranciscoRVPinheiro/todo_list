import os
import dotenv
import requests

dotenv.load_dotenv()

def login():
    url = "https://todoapp-nestjs.adaptable.app/users/login"

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    payload = {
        "email": email,
        "password": password
    }

    request = requests.post(url, json=payload)

    if request.status_code == 201:
        token = request.json()["access_token"]
        print("\nLogin successfull!\n")
        print("Your token is: " + token)
        print("\nPlease add this token to your .env file\n")
    else:
        print(request)

def get_payload():
    title = input("Title: ")
    description = input("Description: ")
    status = input("Status: 1 - not started, 2 - in progress, 3 - completed: ")

    if status == "1":
        status = "not started"
    elif status == "2":
        status = "in progress"
    elif status == "3":
        status = "completed"

    return title, description, status

def create_todo():
    url = "https://todoapp-nestjs.adaptable.app/todos"

    token = os.getenv("TOKEN")

    headers = {"Authorization": "Bearer " + token}

    title, description, status = get_payload()

    payload = {
        "title": title,
        "description": description,
        "status": status
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Todo created successfully!")
    else:
        print(response)


def get_todos():
    url = "https://todoapp-nestjs.adaptable.app/todos"

    token = os.getenv("TOKEN")

    request = requests.get(url, headers={"Authorization": "Bearer " + token})

    if request.status_code == 200:
        for todo in request.json():
            print(f'Id: {todo["_id"]}')
            print(f'Title: {todo["title"]}')
            print(f'Description: {todo["description"]}')
            print(f'Status: {todo["status"]}')
            print("-----------\n")
    else:
        print(request)


def delete_todo(id):
    url = "https://todoapp-nestjs.adaptable.app/todos/" + id

    token = os.getenv("TOKEN")

    request = requests.delete(url, headers={"Authorization": "Bearer " + token})

    if request.status_code == 200:
        print("Todo deleted successfully!")
    else:
        print(request)


def patch_todo(id):
    url = "https://todoapp-nestjs.adaptable.app/todos/" + id

    token = os.getenv("TOKEN")

    title, description, status = get_payload()

    payload = {
        "title": title,
        "description": description,
        "status": status
    }

    request = requests.patch(url, payload, headers={"Authorization": "Bearer " + token})

    if request.status_code == 200:
        print("Todo updated successfully!")
    else:
        print(request)


while True:
    print("1. Login")
    print("2. Create todo")
    print("3. Get todos")
    print("4. Delete todo")
    print("5. Update todo")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        login()
    elif choice == "2":
        create_todo()
    elif choice == "3":
        get_todos()
    elif choice == "4":
        id = input("Enter todo id: ")
        delete_todo(id)
    elif choice == "5":
        id = input("Enter todo id: ")
        patch_todo(id)
    elif choice == "6":
        break
    else:
        print("Invalid choice!")


