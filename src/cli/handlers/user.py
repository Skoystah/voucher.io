from getpass import getpass

from cli.errors import error_message
from config import Config
from user.auth import hash_user_password
from user.models import UserDB


def handle_add_user(config: Config, *args) -> None:
    print("Enter (unique) user name:")
    user_name = input()

    user_password = ""
    while not user_password:
        user_password = getpass("Enter password:")

    user_password = hash_user_password(user_password)

    user_is_admin = ""
    while user_is_admin not in ("y", "n"):
        print("Admin user? (y/n)")
        user_is_admin = input()

    user_is_admin = user_is_admin == "y"

    userDB = UserDB(config)

    try:
        new_user = userDB.add_user(user_name, user_password, user_is_admin)
        print(f"Added user {new_user.name} | Admin = {new_user.is_admin}")
    except KeyError as e:
        print(f"Error - {error_message(e)}")


def handle_manage_user(config: Config, *args) -> None:
    print("Enter user name:")
    user_name = input()

    # user_password = ""
    # while not user_password:
    #     user_password = getpass("Enter current password:")

    userDB = UserDB(config)

    try:
        user = userDB.get_user(user_name)
    except KeyError as e:
        print(f"Error - {error_message(e)}")
        return

    # if not check_user_password(user_password, user.password):
    #     print("Password does not match")
    #     return

    new_user_password = ""
    new_user_password_confirm = ""
    while not new_user_password:
        new_user_password = getpass("Enter new password:")
    while not new_user_password_confirm:
        new_user_password_confirm = getpass("Enter new password to confirm:")

    if new_user_password != new_user_password_confirm:
        print("Password does not match")
        return

    new_user_password_hashed = hash_user_password(new_user_password)
    try:
        userDB.update_user(user.id, new_user_password_hashed)
        print("Password changed succesfully!")
    except KeyError as e:
        print(f"Error - {error_message(e)}")
