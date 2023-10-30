import abc
from validation.base import Validator as BaseValidator


VALIDATION_MESSAGES = {
    "string": "The {field} field must be a string.",
    "required": "The {field} field is required.",
    "integer": "The {field} field must be an integer.",
    "float": "The {field} field must be a float.",
    "min": {
        "string": "The {field} field must be at least {value} characters.",
        # "iterable": "The {field} field must have at least {value} items.",
        "numeric": "The {field} field must be at least {value}.",
    },
    "in": "The {field} field must be one of the following: {values}.",
}


class ValidationMessage(BaseValidator):
    def get_rule_message(self, field, rule) -> str:
        message = VALIDATION_MESSAGES.get(rule)

        if message is None:
            raise KeyError("The rule is not valid.")

        if isinstance(message, dict):
            return message[self.get_field_type(field)]

        return message
