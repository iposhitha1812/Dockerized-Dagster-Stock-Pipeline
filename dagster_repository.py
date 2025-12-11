from dagster import repository
from pipelines.stock_pipeline import stock_job,hourly_schedule

@repository
def repo():
    return [stock_job,hourly_schedule]
