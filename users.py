from fastapi_users import BaseUserManager, UUIDIDMixin
from models import User

SECRET = "SUPER_SECRET_CHANGE_ME"


class UserManager(UUIDIDMixin, BaseUserManager[User, str]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
