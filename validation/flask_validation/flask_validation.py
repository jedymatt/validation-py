from typing import Iterable

from flask import Flask, flash, make_response, redirect, request, session

from validation.errors import ValidationError
from validation.validation import Validator


class FlaskValidation:
    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        app.register_error_handler(ValidationError, self.handle_validation_error)
        app.before_request(self._before_request)

    def _before_request(self):
        session["previous_url"] = request.url

    def handle_validation_error(self, error: ValidationError):
        if request.is_json:
            return make_response({"errors": error.args[0]}, 422)

        flash(error.args[0], "errors")
        flash(request.form.to_dict(), "old")

        return redirect(request.url)

    def validate(self, rules: dict, before_validation=[]):
        if request.method.lower() in ["post", "put", "patch", "delete"]:
            data = request.form.to_dict()
        else:
            data = request.args.to_dict()

        for transform in before_validation:
            data = transform(data)

        return Validator(data, rules).validate()


def transform_to_primitive_types(fields, data, target_type):
    for field in fields:
        if is_empty(data[field]):
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
