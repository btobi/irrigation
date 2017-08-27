from apscheduler.schedulers.blocking import BlockingScheduler


def run_hourly(method):
    method()
    scheduler = BlockingScheduler()
    scheduler.add_job(method, 'interval', hours=1)
    scheduler.start()


def run_minutely(method):
    method()
    scheduler = BlockingScheduler()
    scheduler.add_job(method, 'interval', minutes=1)
    scheduler.start()

