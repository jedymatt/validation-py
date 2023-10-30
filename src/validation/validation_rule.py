from validation.base import Rule, Validator as BaseValidator
from validation.validation_message import VALIDATION_MESSAGES


class ClosureValidationRule(Rule):
    def __init__(self, callback) -> None:
        self.failed = False
        self.callback = callback
        self._message = ""

    def passes(self, field, value) -> bool:
        self.failed = False

        def fail(message: str):
            self.failed = True
            self._message = message

        self.callback(field, value, fail)

        return not self.failed

    def message(self) -> str:
        return self._message


class ConditionalValidationRule(Rule):
    def __init__(self, callback, *parameters) -> None:
        self._rule = callback
        self._parameters = parameters
        self._message = ""

    def passes(self, field, value) -> bool:
        self._field = field

        return self._rule(field, value, *self._parameters)

    def set_message(self, message):
        self._message = message

        return self

    def message(self) -> str:
        return self._message

    def set_validator(self, validator: BaseValidator):
        self._validator = validator

        return self
