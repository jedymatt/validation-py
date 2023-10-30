from typing import Iterable

from flask import Flask, make_response, redirect, request, session

from validation.errors import ValidationError
from validation.validation import Validator

__OLD__ = "__old__"
__ERRORS__ = "__errors__"
__FLASH_REMOVE__ = "__flash_remove__"


def _old(key=None):
    if key is None:
        return session.get(__OLD__, {})

    return session.get(__OLD__, {}).get(key, "")


def _error(key=None):
    if key is None:
        return session.get(__ERRORS__, {})

    return session.get(__ERRORS__, {}).get(key, "")


class FlaskValidation:
    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        app.register_error_handler(ValidationError, self._handle_validation_error)
        app.before_request(self._before_request)
        app.context_processor(self._context_processor)
        self._exclude_from_session: tuple[str] = ()
        self._data = {}

    def _before_request(self):
        session[__FLASH_REMOVE__] = session.get(__FLASH_REMOVE__, False)

        if not session[__FLASH_REMOVE__]:
            session[__FLASH_REMOVE__] = True
        elif session[__FLASH_REMOVE__]:
            for i in [__ERRORS__, __OLD__]:
                if session.get(i, None):
                    session.pop(i)

            session[__FLASH_REMOVE__] = False

        session["previous_url"] = request.url

    def _context_processor(self):
        return {
            "error": _error,
            "old": _old,
        }

    # middleware that excludes fields to not be saved in session
    def exclude_from_session(self, *fields: str):
        def wrapper(f):
            self._exclude_from_session = fields
            return f

        self._exclude_from_session = []
        return wrapper

    def _handle_validation_error(self, error: ValidationError):
        if request.is_json:
            return make_response({"errors": error.args[0]}, 422)

        session[__ERRORS__] = error.args[0]
        session[__OLD__] = {
            k: v
            for k, v in self._data.items()
            if k not in self._exclude_from_session and v is not None
        }
        session[__FLASH_REMOVE__] = False

        return redirect(request.url)

    def validate(self, rules: dict, before_validation=[]):
        if request.is_json:
            self._data = request.json
        else:
            self._data = request.form.to_dict()

        for transform in before_validation:
            self._data = transform(self._data)

        return Validator(self._data, rules).validate()


def transform_to_primitive_types(fields, data, target_type):
    for field in fields:
        if is_empty(data.get(field)):
            continue

        if field in data:
            try:
                # check if type
                if isinstance(data[field], target_type):
                    continue

                data[field] = target_type(data[field])
            except ValueError:
                pass
            except TypeError:
                pass
        else:
            raise ValueError(f"Field {field} does not exist in data")

    return data


def convert_empty_to_none(data):
    return {k: None if is_empty(v) else v for k, v in data.items()}


def is_empty(value):
    if isinstance(value, str):
        return not value.strip()

    if isinstance(value, Iterable):
        return len(value) == 0

    return value is None
