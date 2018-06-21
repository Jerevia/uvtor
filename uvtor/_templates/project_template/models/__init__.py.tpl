from playhouse import postgres_ext
from uvtor.db.models import BaseModel as _BaseModel
import datetime


class BaseModel(_BaseModel):

    created = postgres_ext.DateTimeTZField(
        verbose_name='添加时间',
        default=datetime.datetime.now,
        null=False)
    modified = postgres_ext.DateTimeTZField(
        verbose_name='更新时间',
        default=datetime.datetime.now,
        null=False)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
