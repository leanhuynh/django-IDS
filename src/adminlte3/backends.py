import bcrypt
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class BcryptBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Tìm người dùng theo email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        print(password, user.password)
        # Kiểm tra mật khẩu bằng bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8 ')):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
