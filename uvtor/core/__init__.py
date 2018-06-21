from uvtor.conf import settings
import tornado.web
import pkgutil
import importlib


def make_app(appname, autoreload=True):
    _settings = {'cookie_secret': settings.COOKIE_SECRET, 'xsrf_cookies': True}
    app = tornado.web.Application(
        auto_discover(appname),
        debug=settings.DEBUG,
        autoreload=autoreload,
        **_settings)
    print(auto_discover(appname))
    return app


def auto_discover(appname):
    routes = importlib.import_module('apps.{}.routes'.format(appname))
    name = routes.__name__

    _routes = []
    for loader, modname, ispkg in pkgutil.walk_packages(routes.__path__):
        _module = loader.find_module(modname).load_module(modname)
        if not hasattr(_module, 'routes'):
            continue
        for _, _handler in _module.routes:
            if settings.DEBUG:
                if _ == r'^$':
                    _ = '^%s' % ('%s.%s' % (name, modname)).replace(
                        '.', '/').replace(
                        f'apps/{appname}/routes',
                        f'/api/{appname}')
                else:
                    _ = _.replace(
                        '^/', '^%s/' %
                        ('%s.%s' %
                         (name, modname)).replace(
                            '.', '/').replace(
                            f'apps/{appname}/routes',
                            f'/api/{appname}'))
            else:
                if _ == r'^$':
                    _ = '^%s' % ('%s.%s' % (name, modname)).replace(
                            '.', '/').replace(
                            'apps/{}/routes'.format(appname), '')
                else:
                    _ = _.replace(
                        '^/',
                        '^%s/' % ('%s.%s' % (name, modname)).replace(
                            '.', '/').replace(
                            'apps/{}/routes'.format(appname), ''))
            _routes.append((_, _handler))
    return _routes
