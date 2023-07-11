def user_token():
    with open('tokens.txt', 'r') as file:
        user_token = file.readline().strip()
    return user_token

def group_token():
    with open('tokens.txt', 'r') as file:
        user_token = file.readline().strip()
        group_token = file.readline().strip()
    return group_token

def host():
    db_localhost = '127.0.0.1'
    return db_localhost

def user():
    user = 'postgres'
    return user

def password():
    db_password = '7753191qq'
    return db_password

def db_name():
    name = 'vkbot'
    return name

print(user_token())
print()
print(group_token())