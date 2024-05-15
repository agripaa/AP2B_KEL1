from models.database import load_data, save_data


def add_user(user):
    data = load_data()
    data["users"].append(user)
    save_data(data)


def get_user_by_username(username):
    data = load_data()
    for user in data["users"]:
        if user["username"] == username:
            return user
    return None


def get_user_by_email(email):
    data = load_data()
    for user in data["users"]:
        if user["email"] == email:
            return user
    return None
