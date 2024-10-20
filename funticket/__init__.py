import redis
from django.conf import settings

# Connect to our Redis instance
_redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT, db=6,
)
