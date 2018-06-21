from io import StringIO
import nginx
import pkgutil
import configparser
import os
import getpass


def create_nginx_config(
        domain,
        listen,
        log_dir,
        start_port=4500):
    conf = nginx.Conf()
    _apps = __import__('apps')
    _port = start_port
    _server = nginx.Server()
    _server.add(
        nginx.Key('listen', listen),
        nginx.Key('server_name', domain),
        nginx.Key('client_max_body_size', '10m'),

    )
    for loader, module_name, is_pkg in pkgutil.iter_modules(_apps.__path__):
        _module = loader.find_module(module_name).load_module(module_name)
        if hasattr(_module, '__APPID__'):
            _appid = _module.__APPID__
        else:
            _appid = module_name.replace('_', '-')
        _n_workers = _module.__WORKERS__
        _upstream = []
        for _i in range(_n_workers):
            _upstream.append(nginx.Key('server', f'127.0.0.1:{_port}'))
            _port += 1
        conf.add(nginx.Upstream(
            _appid, *_upstream
            )
        )
        _server.add(
            nginx.Location(
                f'~ ^/api/{_appid}/v[0-9]/',
                nginx.Key('rewrite', f'^/api/{_appid}/(.*) /$1  break'),
                nginx.Key('proxy_pass', f'http://{_appid}'),
                nginx.Key('proxy_http_version', '1.1'),
                nginx.Key('proxy_set_header', 'Upgrade $http_upgrade'),
                nginx.Key('proxy_set_header', 'Connection "upgrade"'),
                nginx.Key('proxy_set_header', 'X-real-ip $remote_addr'),
                nginx.Key('proxy_set_header', 'X-Forwarded-For $remote_addr'),
            )
        )
    conf.add(
        nginx.Key('access_log', os.path.join(log_dir, f'apis-access.log'))
    )
    conf.add(_server)
    return nginx.dumps(conf)


def create_supervisor_config(
        log_dir,
        user=getpass.getuser(),
        directory=os.getcwd(),
        start_port=4500):
    config = configparser.SafeConfigParser()
    _programs = []
    _apps = __import__('apps')
    _port = start_port

    for loader, module_name, is_pkg in pkgutil.iter_modules(_apps.__path__):
        _module = loader.find_module(module_name).load_module(module_name)
        if hasattr(_module, '__APPID__'):
            _appid = _module.__APPID__
        else:
            _appid = module_name
        _n_workers = _module.__WORKERS__
        for _i in range(_n_workers):
            _ = {}
            _['directory'] = directory
            _['command'] = (
                f'/home/{user}/anaconda3/bin/python'
                f' -u -m uvtor runapp {module_name} --port={_port}')
            _['user'] = user
            _['autostart'] = 'true'
            _['autorestart'] = 'true'
            _['stopasgroup'] = 'true'
            _['killasgroup'] = 'true'
            _['redirect_stderr'] = 'true'
            _['stdout_logfile'] = os.path.join(
                log_dir, f'{module_name}_api.log')
            _['stdout_logfile_maxbytes'] = '200MB'
            _['stdout_logfile_backups'] = 5
            _['loglevel'] = 'INFO'
            _['environment'] = 'DEBUG="False",PYTHONIOENCODING="utf-8"'
            config[f'program:{_appid}{_i}'] = _
            _programs.append(f'{_appid}{_i}')
            _port += 1
    config['group:apis'] = {
        'programs': ','.join(_programs)
    }
    with StringIO() as _io:
        config.write(_io)
        return _io.getvalue()
