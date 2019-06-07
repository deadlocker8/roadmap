class UserService:
    def __init__(self, users):
        self.__users = {}
        for user in users:
            self.__users[user["name"]] = user["password"]

    def get_users(self):
        return self.__users

    def get_password_by_username(self, name):
        return self.__users.get(name, None)
