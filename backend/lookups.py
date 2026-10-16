import whois
import dns.resolver
from datetime import datetime


def check_dns(domain):
    try:
        dns.resolver.resolve(domain, "A")
        return 1
    except Exception:
        return -1


def to_date(value):
    if isinstance(value, list):
        value = value[0]
    return value.replace(tzinfo=None)


def check_whois(domain):
    try:
        info = whois.whois(domain)
        created = to_date(info.creation_date)
        expires = to_date(info.expiration_date)
        today = datetime.now()

        age_days = (today - created).days
        days_left = (expires - today).days

        age = 1 if age_days >= 180 else -1
        reg_length = 1 if days_left > 365 else -1
        return age, reg_length
    except Exception:
        return -1, -1