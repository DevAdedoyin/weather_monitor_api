



from datetime import UTC, datetime, timedelta

from sqlalchemy import select

import database
import models


INACTIVITY_DAYS = 30


def cleanup_inactive_chats() -> int:
    cutoff_date = datetime.now(UTC) - timedelta(
        days=INACTIVITY_DAYS
    )

    with database.SessionLocal() as db:
        try:
            inactive_chats = db.scalars(
                select(models.UserChat).where(
                    models.UserChat.is_authenticated.is_(False),
                    models.UserChat.last_used < cutoff_date,
                )
            ).all()

            deleted_count = len(inactive_chats)

            for chat in inactive_chats:
                db.delete(chat)

            db.commit()

            print(
                f"Cleanup completed. "
                f"Deleted {deleted_count} inactive chat sessions."
            )

            return deleted_count

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    cleanup_inactive_chats()
