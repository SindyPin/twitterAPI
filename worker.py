import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://h:pb857b6aec997348dae5b563101c5bd848c7035a575e659310d850cc090ef2394@ec2-3-82-83-129.compute-1.amazonaws.com:23679')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
