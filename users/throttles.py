from rest_framework.throttling import AnonRateThrottle


class PasswordLoginRateThrottle(AnonRateThrottle):
    scope = 'login'
    rate = '10/minute'


class OTPRateThrottle(AnonRateThrottle):
    scope = 'otp'
    rate = '4/minute'
