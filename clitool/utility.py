import json
def search_user(username):
    with open("users.txt",'r') as file:
        data=json.load(file)
        print(data)