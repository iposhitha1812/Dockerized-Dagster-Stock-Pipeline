from dagster import job, op, schedule
from fetcher.fetch_and_store import fetch_and_store

@op
def fetch_op(context):
    result = fetch_and_store(context.log)
    return result

@job
def stock_job():
    fetch_op()

# hourly schedule (run at minute 0 every hour)
@schedule(cron_schedule="0 * * * *", job=stock_job, execution_timezone="Asia/Kolkata")
def hourly_schedule(_context):
    return {}
