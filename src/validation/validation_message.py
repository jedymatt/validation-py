import abc
from typing import Any, Callable, TypeVar
from validation.base import Validator as BaseValidator
from validation.rules import rule_name


VALIDATION_MESSAGES = {
    "string": "The {field} field must be a string.",
    "required": "The {field} field is required.",
    "integer": "The {field} field must be an integer.",
    "float": "The {field} field must be a float.",
    "min": {
        "string": "The {field} field must be at least {min} characters.",
        # "iterable": "The {field} field must have at least {min} items.",
        "numeric": "The {field} field must be at least {min}.",
    },
    "max": {
        "string": "The {field} field must not exceed {max} characters.",
        # "iterable": "The {field} field must not have more than {max} items.",
        "numeric": "The {field} field must not be greater than {max}.",
    },
    "in": "The {field} field must be one of the following: {values}.",
}


class MessageReplacer:
    def replace_min(self, message, field, rule, params):
        return message.replace("{min}", str(params[0]))


class ValidationMessage(MessageReplacer, BaseValidator):
    def get_message(self, field, rule: Callable):
        if rule in self.size_rules:
            return self.get_size_message(field, rule)

        return VALIDATION_MESSAGES[rule_name(rule)]

    def get_size_message(self, field: str, rule: Callable):
        return VALIDATION_MESSAGES[rule_name(rule)][self.get_field_type(field)]

    def format_message(
        self, message: str, field: str, rule: Callable, *params: Any
    ) -> str:
        message = message.replace("{field}", field)

        if hasattr(self, f"replace_{rule_name(rule)}"):
            message = getattr(self, "replace_" + rule_name(rule))(
                message, field, rule, params
            )

        return message
