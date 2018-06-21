from uvtor.core import response as _resp
from uvtor.core.exceptions import APIException
import traceback


def standard_api(func):

    async def decorator(client, *args, **kwargs):
        try:
            result = await func(client, *args, **kwargs)
            if isinstance(result, dict) or not result:
                response = {'code': _resp.CODE_0_SUCCESS}
                response.update(result or {})
                client.write(response)
            else:
                client.write(result)
        except (APIException, Exception) as e:
            # print(traceback.format_exc())
            if not hasattr(e, 'code'):
                print(traceback.format_exc())
                e.code = 1
            client.write({'code': e.code, 'error_msg': str(e)})

    return decorator
