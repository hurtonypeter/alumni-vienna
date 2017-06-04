from apscheduler.schedulers.blocking import BlockingScheduler

from rq import Queue
from worker import conn

from tasks import send_newsletter

sched = BlockingScheduler()

q = Queue(connection=conn)

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    q.enqueue(send_newsletter)

sched.start()