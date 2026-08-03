import time
from django.core.cache import cache
from django.http import HttpResponse
GENERAL_WINDOW_SECONDS = 60
GENERAL_MAX_REQUESTS = 3000
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
        bucket = int(time.time() // window_seconds)
        key = f"ss:{scope}:{ip}:{bucket}"
        try:
            count = cache.incr(key)
        except ValueError:
            try:
                cache.add(key, 0, timeout=window_seconds + 5)
                count = cache.incr(key)
            except Exception:
                return False  
        except Exception:
            return False  
        return count > max_requests