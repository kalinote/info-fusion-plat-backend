class EmptyResponseException(Exception):
    """返回数据为空
    """

class TokenNotExistException(Exception):
    """token不存在
    """

class StatusError(Exception):
    """请求返回数据错误
    """
