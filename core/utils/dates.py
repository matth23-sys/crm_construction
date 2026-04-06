from datetime import datetime, time, timedelta

from django.utils import timezone


def aware_now():
    return timezone.localtime()


def local_today():
    return timezone.localdate()


def day_bounds(target_date):
    start = timezone.make_aware(datetime.combine(target_date, time.min))
    end = timezone.make_aware(datetime.combine(target_date, time.max))
    return start, end


def is_within_next_hours(target_datetime, hours):
    now = aware_now()
    limit = now + timedelta(hours=hours)
    return now <= target_datetime <= limit