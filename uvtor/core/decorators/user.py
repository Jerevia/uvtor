from uvtor.core import exceptions


async def _check_login(client):
    _user = await client.get_current_user()
    if not _user:
        raise exceptions.LoginRequired
    return _user


def ensure_xsrf(func):

    async def decorator(client, *args, **kwargs):
        client.set_cookie('_xsrf', client.xsrf_token)
        return await func(client, *args, **kwargs)

    return decorator


def login_required(func):

    async def decorator(client, *args, **kwargs):
        await _check_login(client)
        return await func(client, *args, **kwargs)

    return decorator
