from apscheduler.schedulers.background import BackgroundScheduler
from app.services.email_service import send_reminder_email
from app.services.messages import get_random_message

scheduler = BackgroundScheduler()
scheduler.start()


def add_job(reminder_id, cron_expr, email, message, reminder_type):
    minute, hour, day, month, dow = cron_expr.split()

    # ✅ wrapper task
    def task():
        final_message = get_random_message(reminder_type, message)

        # ✅ use new HTML email function
        send_reminder_email(email, final_message)

    scheduler.add_job(
        task,
        trigger="cron",
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=dow,
        id=str(reminder_id),
        replace_existing=True
    )


def remove_job(reminder_id: str):
    try:
        scheduler.remove_job(reminder_id)
    except Exception:
        pass