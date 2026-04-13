import http.cookiejar

from .. import config
from . import coreutils


# Custom policies for cookies

ALLOWED_DOMAINS = coreutils.domains_from_files(config.PATH_COOKIES_ALLOW)


class RejectAllCookiePolicy(http.cookiejar.DefaultCookiePolicy):
    def set_ok(self, cookie, request):
        return False


class AllowAllCookiePolicy(http.cookiejar.DefaultCookiePolicy):
    def set_ok(self, cookie, request):
        return True


class StrictAllowCookiePolicy(http.cookiejar.DefaultCookiePolicy):
    """Only allow cookies for domains that are known to not work without them."""
    def set_ok(self, cookie, request):
        if cookie.domain in ALLOWED_DOMAINS:
            return super().set_ok(cookie, request)
        return False


COOKIE_REJECT_ALL = RejectAllCookiePolicy()
COOKIE_ALLOW_ALL = AllowAllCookiePolicy()
COOKIE_STRICT_ALLOW = StrictAllowCookiePolicy()
