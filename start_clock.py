from zqfa.worker.clock import sched
from zqfa.worker.tasks import send_newsletter

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    send_newsletter()

sched.start()
