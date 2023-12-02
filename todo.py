import os
import dotenv
import requests
from rich import print

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
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    status = input("Status: 1 - not started, 2 - in progress, 3 - completed: ").strip()

    if len(description) == 0:
        description = 'No description provided.'

    if status == "1":
        status = "not started"
    elif status == "2":
        status = "in progress"
    elif status == "3":
        status = "completed"
    else:
        raise Exception("[red]Invalid input![/red]")

    return title, description, status

def create_todo(token):
    url = "https://todoapp-nestjs.adaptable.app/todos"

    headers = {"Authorization": "Bearer " + token}

    title, description, status = get_payload()

    payload = {
        "title": title,
        "description": description,
        "status": status
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("[green]Todo created successfully![/green]")
    else:
        print(response)


def get_todos(token):
    url = "https://todoapp-nestjs.adaptable.app/todos"

    request = requests.get(url, headers={"Authorization": "Bearer " + token})

    if request.status_code == 200:
        for todo in request.json():
            print("\n-------------------------------------")
            print(f'Id: {todo["_id"]}')
            print(f'Title: {todo["title"]}')
            print(f'Description: {todo["description"]}')
            print(f'Status: [green]{todo["status"]}[/green]')
            print("-------------------------------------\n")
    else:
        print(request)


def delete_todo(id, token):
    url = "https://todoapp-nestjs.adaptable.app/todos/" + id

    request = requests.delete(url, headers={"Authorization": "Bearer " + token})

    if request.status_code == 200:
        print("[green]Todo deleted successfully![/green]")
    else:
        print(request)


def patch_todo(id, token):
    url = "https://todoapp-nestjs.adaptable.app/todos/" + id

    title, description, status = get_payload()

    payload = {
        "title": title,
        "description": description,
        "status": status
    }

    request = requests.patch(url, payload, headers={"Authorization": "Bearer " + token})

    if request.status_code == 200:
        print("[green]Todo updated successfully![/green]")
    else:
        print(request)

if __name__ == "__main__":

    token = os.getenv("TOKEN")

    while True:
        print("1. Login")
        print("2. Create todo")
        print("3. Get todos")
        print("4. Delete todo")
        print("5. Update todo")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            login()
        elif choice == "2":
            create_todo(token)
        elif choice == "3":
            get_todos(token)
        elif choice == "4":
            id = input("Enter todo id: ")
            delete_todo(id, token)
        elif choice == "5":
            id = input("Enter todo id: ")
            patch_todo(id, token)
        elif choice == "0":
            break
        else:
            print("[red]Invalid choice![/red]")


