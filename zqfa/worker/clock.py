from apscheduler.schedulers.blocking import BlockingScheduler

from rq import Queue
from zqfa.worker.worker import conn

sched = BlockingScheduler()

queue = Queue(connection=conn)

