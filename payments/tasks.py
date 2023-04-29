import project.settings
from project.celery import app
import yagmail

@app.task()
def send_email_task():
    yag = yagmail(project.settings.EMAIL_HOST_USER, project.settings.EMAIL_HOST_PASSWORD)