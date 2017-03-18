import logbook

import show_off_web_app.infrastructure.static_cache as static_cache
import pyramid.httpexceptions as exc

from show_off_web_app.infrastructure.supressor import suppress
import show_off_web_app.infrastructure.cookie_auth as cookie_auth
from show_off_web_app.services.account_service import AccountService


class BaseController:
    def __init__(self, request):
        self.request = request
        self.build_cache_id = static_cache.build_cache_id

        log_name = 'Ctrls/' + type(self).__name__.replace("Controller", "")
        self.log = logbook.Logger(log_name)

    @property
    def is_logged_in(self):
        return cookie_auth.get_user_id_via_auth_cookie(self.request) is not None

    # noinspection PyMethodMayBeStatic
    @suppress()
    def redirect(self, to_url, permanent=False):
        if permanent:
            raise exc.HTTPMovedPermanently(to_url)
        raise exc.HTTPFound(to_url)

    @property
    def merged_dicts(self):
        data = dict()
        data.update(self.request.GET)
        data.update(self.request.POST)
        data.update(self.request.matchdict)

        return data

    @property
    def logged_in_user_id(self):
        user_id = cookie_auth.get_user_id_via_auth_cookie(self.request)
        return user_id

    @property
    def logged_in_user(self):
        uid = self.logged_in_user_id
        if not uid:
            return None

        return AccountService.find_account_by_id(uid)
