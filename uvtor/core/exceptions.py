from uvtor.core import response as _resp


class APIException(Exception):

    code = _resp.CODE_1_ERROR
    default_detail = 'A server error occurred.'
    default_detail_zh = '服务器发生了一个错误'

    def __init__(self, detail=None, chinese_detail=True):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail
            if chinese_detail:
                self.detail = self.default_detail_zh

    def __str__(self):
        return self.detail


class LoginRequired(APIException):
    code = _resp.CODE_2_LOGIN_REQUIRED
    default_detail = 'Login required.'

    default_detail_zh = '请登陆后再进行此操作'


class SecureTokenError(APIException):

    code = _resp.CODE_3_ERROR_SECURE_TOKEN
    default_detail = 'Error secure token.'


class UsernameOrPasswordError(APIException):

    code = _resp.CODE_4_ERROR_USERNAME_OR_PASSWORD
    default_detail = 'Error username or password.'

    default_detail_zh = '错误的用户名或密码'


class InvalidPassword(APIException):

    code = _resp.CODE_5_INVALID_PASSWORD
    default_detail = 'Invalid password'

    default_detail_zh = '密码不符合要求'


class UserCreationError(APIException):

    code = _resp.CODE_6_USER_CREATION_FAILED
    default_detail = 'UserCreationError.'

    default_detail_zh = '创建用户失败'


class SMSSendFailed(APIException):

    code = _resp.CODE_7_SEND_SMS_FAILED
    default_detail = 'Send SMS failed'

    default_detail_zh = '短信发送失败'


class CaptchaValidationError(APIException):

    code = _resp.CODE_8_CAPTCHA_VALIDATION_ERROR
    default_detail = 'Captcha validation error'

    default_detail_zh = '验证码不匹配'


class InvalidPhoneNumber(APIException):

    code = _resp.CODE_9_INVALID_PHONE_NUMBER
    default_detail = 'Invalid phone number'

    default_detail_zh = '不正确的手机号码'


class InvalidEmailAddress(APIException):

    code = _resp.CODE_10_INVALID_EMAIL_ADDRESS
    default_detail = 'Invalid email address'

    default_detail_zh = '不正确的邮件地址'


class InvalidUsername(APIException):

    code = _resp.CODE_11_INVALID_USERNAME
    default_detail = 'Invalid username'

    default_detail_zh = '不合法的用户名'


class InvalidChineseName(APIException):

    code = _resp.CODE_12_INVALID_CHINESE_NAME
    default_detail = 'Invalid Chinese name'

    default_detail_zh = '不正确的中文姓名'


class VcodeValidationError(APIException):

    code = _resp.CODE_13_VCODE_VALIDATION_ERROR
    default_detail = 'Vcode validation error'

    default_detail_zh = '验证码不正确或已经失效'


class PhoneAlreadyExistsError(APIException):

    code = _resp.CODE_14_PHONE_ALREADY_EXISTS_ERROR
    default_detail = 'Phone already exists'

    default_detail_zh = '手机号已经被注册'


class UsernameAlreadyExistsError(APIException):

    code = _resp.CODE_15_USERNAME_ALREADY_EXISTS_ERROR
    default_detail = 'Username already exists'

    default_detail_zh = '用户名已存在'


class EmailAlreadyExistsError(APIException):

    code = _resp.CODE_16_EMAIL_ALREADY_EXISTS_ERROR
    default_detail = 'Email already exists'

    default_detail_zh = '邮箱地址已经被注册'


class MissingRequiredParams(APIException):

    code = _resp.CODE_19_MISSING_REQUIRED_PARAMS
    default_detail = 'Required params is missing'

    default_detail_zh = '缺少必要参数'


class PermissionDenied(APIException):

    code = _resp.CODE_20_PERMISSION_DENIED
    default_detail = 'Permission denied'

    default_detail_zh = '没有权限查看此内容'


class InvalidParameterValue(APIException):

    code = _resp.CODE_21_INVALID_PARAMETER
    default_detail = 'Invalid parameter value'

    default_detail_zh = '不正确的参数值'


class ObjectAlreadyExists(APIException):

    code = _resp.CODE_23_OBJECT_ALREADY_EXISTS
    default_detail = 'Object already exists'

    default_detail_zh = '此项已经存在'


class UserIsDisabled(APIException):

    code = _resp.CODE_24_USER_IS_DISABLED
    default_detail = 'The user is disabled'

    default_detail_zh = '该用户已被禁用'


class ObjectNotFound(APIException):

    code = _resp.CODE_25_OBJECT_NOT_FOUND
    default_detail = 'Object not found'

    default_detail_zh = '未找到指定资源'
