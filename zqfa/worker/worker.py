import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://redistogo:44a620cf0a725714891715acc24d5ea6@greeneye.redistogo.com:9302/')

conn = redis.from_url(redis_url)
