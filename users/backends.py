from django.contrib.auth.backends import ModelBackend
from . import _redis_instance
from .models import User
from .redis_keys import _OTP_KEY

# When User Login in django admin


class UserBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return
        try:
            user = User.objects.get(username=username)
            otp = _redis_instance.get(_OTP_KEY.format(user_pk=user.id))
            if otp is None:
                return
            if otp.decode('utf-8') == password:
                _redis_instance.delete(_OTP_KEY.format(user_pk=user.id))
                return user
        except User.DoesNotExist:
            pass
