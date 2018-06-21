from playhouse import postgres_ext
from uvtor.core import exceptions
from uvtor.core.cache import cache
from uvtor.conf import settings
from utilib.utils import security
from utilib.utils import timezone
from uvtor.db.models import manager
from uvtor.db.models import BaseModel
from datetime import datetime
import peewee
import base64
import uuid
import pickle


class User(BaseModel):
    date_joined = postgres_ext.DateTimeField(default=datetime.now())
    email = postgres_ext.CharField(null=True, unique=True)
    first_name = postgres_ext.CharField(null=True)
    is_active = postgres_ext.BooleanField(default=True)
    is_superuser = postgres_ext.BooleanField(default=False)
    last_login = postgres_ext.DateTimeField(null=True)
    last_name = postgres_ext.CharField(null=True)
    password = postgres_ext.CharField()
    salt = postgres_ext.CharField()
    phone = postgres_ext.CharField(null=True)
    username = postgres_ext.CharField(unique=True)

    class Meta:
        db_table = '_user'

    def __str__(self):
        return str.format('{username}, {phone}',
                          username=self.username,
                          phone=self.phone)

    def _check_password(self, password):
        return security.get_password(password, self.salt) == self.password

    def check_password(self, password):
        if not self._check_password(password):
            raise exceptions.UsernameOrPasswordError

    async def _set_password(self, password):
        _password, _salt = security.gen_password(password)
        await manager.execute(
            User.update(password=_password,
                        salt=_salt).where(User.id == self.id))

    @staticmethod
    async def create_user(username, password, phone=None, email=None,
                          first_name=None, last_name=None):
        _password, _salt = security.gen_password(password)
        try:
            return await manager.execute(
                User.insert(username=username,
                            password=_password,
                            salt=_salt,
                            phone=phone,
                            email=email,
                            first_name=first_name,
                            last_name=last_name))
        except peewee.IntegrityError:
            raise exceptions.UserCreationError

    @staticmethod
    async def login(_, password, secure_token=None):
        if isinstance(secure_token, bytes):
            secure_token = secure_token.decode()
        try:
            _user = await manager.get(
                User.select().where((User.username == _)
                                    | (User.phone == _)
                                    | (User.email == _)))
            if not _user.is_active:
                raise exceptions.UserIsDisabled
            _user.check_password(password)
        except Exception as e:
            print(e)
            if secure_token:
                await cache.delete(str.format('{}:{}',
                                              settings.SESSION_PREFIX,
                                              secure_token))
            raise exceptions.UsernameOrPasswordError
        _user.last_login = timezone.now()
        login_info = {}
        login_info['login_time'] = timezone.now()
        login_info['user_id'] = _user.id
        _secure = None
        if await cache.get(str.format('{}:{}',
                                      settings.SESSION_PREFIX,
                                      secure_token)):
            _secure = secure_token
        else:
            _secure = base64.b64encode(
                uuid.uuid4().bytes + uuid.uuid4().bytes).decode()
        await cache.set(str.format('{}:{}',
                                   settings.SESSION_PREFIX,
                                   _secure),
                        pickle.dumps(login_info))
        await manager.update(_user)
        return _secure

    async def logout(secure_token):
        if isinstance(secure_token, bytes):
            secure_token = secure_token.decode()
        await cache.delete(str.format('{}:{}',
                                      settings.SESSION_PREFIX,
                                      secure_token))

    @staticmethod
    async def validate(phone=None,
                       username=None,
                       email=None,
                       raise_exception=False):
        users = await manager.execute(
            User.select().where((User.phone == phone)
                                | (User.username == username)
                                | (User.email == email)))
        if len(users) == 0:
            return True
        _phones = [_user.phone for _user in users]
        _usernames = [_user.username for _user in users]
        _emails = [_user.email for _user in users]

        if raise_exception and phone in _phones and phone:
            raise exceptions.PhoneAlreadyExistsError
        elif raise_exception and username in _usernames and username:
            raise exceptions.UsernameAlreadyExistsError
        elif raise_exception and email in _emails and email:
            raise exceptions.EmailAlreadyExistsError
        return False
