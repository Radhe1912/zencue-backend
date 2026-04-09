from apscheduler.schedulers.background import BackgroundScheduler
from app.services.email_service import send_email

scheduler = BackgroundScheduler()
scheduler.start()

def add_job(reminder_id, cron_expr, email, message):
    minute, hour, day, month, dow = cron_expr.split()

    scheduler.add_job(
        send_email,
        trigger='cron',
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=dow,
        args=[email, message],
        id=str(reminder_id),
        replace_existing=True
    )

def remove_job(reminder_id: str):
    try:
        scheduler.remove_job(reminder_id)
    except Exception:
        pass  # job may not exist