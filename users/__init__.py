from django.conf import settings
import redis


default_app_config = 'users.apps.UsersConfig'
# Connect to our Redis instance
_redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT, db=5,
    decode_responses=True,
)
