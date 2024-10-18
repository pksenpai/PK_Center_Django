from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model; User = get_user_model()
from multiprocessing import AuthenticationError


class CustomModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if (username is None or password is None) and not email:
            return None

        if email:
            try:
                user = User._default_manager.get(email=email)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User._default_manager.get_by_natural_key(username)
            except User.DoesNotExist:
                return None

        if password and user.check_password(password) and self.user_can_authenticate(user):
            return user
        elif email and self.user_can_authenticate(user):
            return user
        else:
            return None
# """
# Custom authentication backend for login user with OTP code... :3
# """
# def email_authenticate(email):
#     User = get_user_model()
#     try:
#         user = User.objects.get(email=email) or None
#         return user

#     except (User.DoesNotExist, AuthenticationError):
#         # User does not exist, authentication fails
#         return None
