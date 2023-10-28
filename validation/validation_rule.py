import abc
from validation.error_message import ERROR_MESSAGES

class ValidationRule(abc.ABC):
    @abc.abstractmethod
    def passes(self, field, value, message=None) -> bool:
        pass

    @abc.abstractmethod
    def message(self) -> str:
        pass


class ClosureValidationRule(ValidationRule):
    def __init__(self, callback) -> None:
        self.failed = False

        self.callback = callback
        self._message = ""

    def passes(self, field, value) -> bool:
        self.failed = False

        def fail(message=None):
            self.failed = True
            self._message = message or f"{field} is invalid"

        self.callback(field, value, fail)

        return not self.failed

    def message(self) -> str:
        return self._message


class ConditionValidationRule(ValidationRule):
    def __init__(self, callback) -> None:
        self.callback = callback
        self._message = ""

    def passes(self, field, value, message=None) -> bool:
        validation_rule = self.callback.__name__.replace("validate_", "")

        self._message = message or f"{ERROR_MESSAGES[validation_rule]}".format(
            field=field
        )

        return self.callback(value)

    def message(self) -> str:
        return self._message
