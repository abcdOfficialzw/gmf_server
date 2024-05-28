from enum import Enum
from flask import json


class NetworkResponse:
    def __init__(self, status, message, data, is_exception, error_message):
        self.status = status
        self.message = message
        self.data = data
        self.is_exception = is_exception
        self.error_message = error_message

    def to_json(self) -> json:
        return self.__dict__

    def to_string(self) -> str:
        return str(self.__dict__)


class NetworkingStatus(Enum):
    FAILED = "failed"
    SUCCESS = "success"


class HttpStatusCode(Enum):
    OK = 200
    NOT_FOUND = 404
    EXCEPTION = 500
    UNAUTHORIZED = 401
    FORBIDEN = 403