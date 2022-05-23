import json


def support():
    with open('config/config.json', 'r') as file:
        load = json.loads(file.read())
        user = load['user_suporte']
        
        return user


