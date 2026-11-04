from celery import shared_task
from django.core.management import call_command


@shared_task
def run_etl_pipeline():
    call_command("run_etl")