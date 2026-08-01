"""
security_shield.py — Optimized drop-in DoS protection for Django 5.

Calibrated for a hackathon venue where ~650 participants share 1-2 NAT'd
public IPs. Uses atomic fixed-window counters via Django's cache framework
(cheap O(1) cache.incr — no per-request timestamp lists to scan or grow)
and fails open if the cache backend errors or times out, so a Redis/DB
cache outage never turns into a 500 for real users.

Requires CACHES['default'] to point at Redis or a shared DB cache backend
so counts are consistent across Gunicorn workers — if left on the
LocMemCache default, each worker process counts independently.
"""

import time

from django.core.cache import cache
from django.http import HttpResponse

# General traffic limit — calibrated for a shared venue IP.
GENERAL_WINDOW_SECONDS = 60
GENERAL_MAX_REQUESTS = 3000

# Login/registration limit — same shared-IP calibration, longer window.
LOGIN_WINDOW_SECONDS = 15 * 60
LOGIN_MAX_REQUESTS = 800
LOGIN_PATH_PREFIXES = ('/accounts/login/', '/accounts/google/', '/registration/')

_GENERAL_429 = HttpResponse(
    "Too many requests. Please slow down.", status=429, content_type="text/plain"
)
_LOGIN_429 = HttpResponse(
    "Too many attempts. Please wait a few minutes and try again.",
    status=429,
    content_type="text/plain",
)


class SecurityShieldMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self._get_client_ip(request)

        if request.path.startswith(LOGIN_PATH_PREFIXES):
            if self._is_rate_limited("l", client_ip, LOGIN_MAX_REQUESTS, LOGIN_WINDOW_SECONDS):
                return _LOGIN_429

        if self._is_rate_limited("g", client_ip, GENERAL_MAX_REQUESTS, GENERAL_WINDOW_SECONDS):
            return _GENERAL_429

        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",", 1)[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")

    @staticmethod
    def _is_rate_limited(scope, ip, max_requests, window_seconds):
        # Fixed-window counter keyed by IP + time bucket. One or two cheap
        # atomic cache ops per request — no lists, no per-request parsing.
        bucket = int(time.time() // window_seconds)
        key = f"ss:{scope}:{ip}:{bucket}"

        try:
            count = cache.incr(key)
        except ValueError:
            # Key doesn't exist yet for this window — create it.
            try:
                cache.add(key, 0, timeout=window_seconds + 5)
                count = cache.incr(key)
            except Exception:
                return False  # fail open
        except Exception:
            return False  # cache backend down/slow — fail open, never 500

        return count > max_requests
