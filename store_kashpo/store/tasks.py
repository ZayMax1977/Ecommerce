from celery import shared_task

from store_kashpo.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL


@shared_task
def send_email(subject, message ):
	send_email(subject, message , DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
	return
