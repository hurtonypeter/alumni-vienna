from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='sun', hour=0)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()