import whois
import dns.resolver
import ssl
import socket
import time
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
        return None


def check_ssl(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                secure_sock.getpeercert()
        return 1
    except ssl.SSLCertVerificationError:
        return 0
    except Exception:
        return -1


CACHE = {}
CACHE_SECONDS = 24 * 60 * 60


def get_lookups(domain):
    now = time.time()

    if domain in CACHE:
        saved_time, result = CACHE[domain]
        if now - saved_time < CACHE_SECONDS:
            return result

    dns_record = check_dns(domain)
    whois_result = check_whois(domain)

    if whois_result is None:
        if dns_record == 1:
            return None
        whois_result = (-1, -1)

    age, reg_length = whois_result
    ssl_state = check_ssl(domain)

    result = (dns_record, age, reg_length, ssl_state)
    CACHE[domain] = (now, result)
    return result