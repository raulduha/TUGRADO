from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

# Los días de estudio (rachas) se cuentan en la hora de Chile, no en UTC.
CHILE = ZoneInfo("America/Santiago")


def utc_now() -> datetime:
    return datetime.now(UTC)


def chile_date(moment: datetime) -> date:
    return moment.astimezone(CHILE).date()
