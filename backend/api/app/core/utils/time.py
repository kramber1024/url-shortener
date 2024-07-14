from datetime import UTC, datetime


def current_time() -> datetime:
    """Get the current time in UTC+0.

    Returns
    -------
        datetime: The current time in UTC+0.

    """
    return datetime.now(UTC)
