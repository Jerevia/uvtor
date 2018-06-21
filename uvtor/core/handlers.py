from uvtor.conf import settings
from uvtor.core.cache import cache
from uvtor.db.models import manager
from uvtor.db.models.user import User
import tornado.web
import functools
import pickle


class BaseHandler(tornado.web.RequestHandler):

    def check_xsrf_cookie(self):

        if settings.DEBUG:
            return True
        else:
            super(BaseHandler, self).check_xsrf_cookie()

    def _args(self, *keys):
        return map(
            functools.partial(
                self.get_argument, default=None),
            keys)

    def _secure_cookies(self, *keys):
        return map(
            self.get_secure_cookie,
            keys)

    async def get_current_user(self):
        secure_token = self.get_secure_cookie('_secure')
        if not secure_token:
            return None
        if isinstance(secure_token, bytes):
            secure_token = secure_token.decode()
        _ = await cache.get(str.format('{}:{}',
                                       settings.SESSION_PREFIX,
                                       secure_token))
        if not _:
            return None
        _user = pickle.loads(
                _
            )
        if not _user:
            return None
        return await manager.get(User, id=_user.get('user_id'))
