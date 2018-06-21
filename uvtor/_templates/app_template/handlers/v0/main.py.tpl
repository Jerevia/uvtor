from uvtor.core.decorators.api import standard_api
from apps.{appname}.handlers import BaseHandler


class ExampleHandler(BaseHandler):

    @standard_api
    async def get(self):

        return {{
            'data': 'example'
        }}
