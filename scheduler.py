from apscheduler.schedulers.asyncio import AsyncIOScheduler

from cleanup_inactive_chats import cleanup_inactive_chats

scheduler = AsyncIOScheduler(timezone="Africa/Lagos")


def start_scheduler():
    scheduler.add_job(
        cleanup_inactive_chats,
        trigger="cron",
        hour=2,
        minute=0,
        id="cleanup_inactive_chats",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)