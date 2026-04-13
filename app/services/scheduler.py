from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

from app.services.email_service import send_reminder_email
from app.services.messages import get_random_message


scheduler = BackgroundScheduler()
scheduler.start()


def add_job(reminder_id, cron_expr, email, message, reminder_type):
    def task():
        final_message = get_random_message(reminder_type, message)
        send_reminder_email(email, final_message, reminder_type)

    if cron_expr.startswith("ONCE|"):
        run_at = datetime.fromisoformat(cron_expr.split("|", 1)[1])
        scheduler.add_job(
            task,
            trigger=DateTrigger(run_date=run_at),
            id=str(reminder_id),
            replace_existing=True,
        )
        return

    parts = cron_expr.split()

    if len(parts) == 5:
        minute, hour, day, month, day_of_week = parts
        year = "*"
    elif len(parts) == 6:
        minute, hour, day, month, day_of_week, year = parts
    else:
        raise ValueError(f"Unsupported schedule format: {cron_expr}")

    scheduler.add_job(
        task,
        trigger="cron",
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week,
        year=year,
        id=str(reminder_id),
        replace_existing=True,
    )


def remove_job(reminder_id: str):
    try:
        scheduler.remove_job(reminder_id)
    except Exception:
        pass
