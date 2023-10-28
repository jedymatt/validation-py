import inspect
from typing import Any
from validation.errors import InvalidRuleError, ValidationError

from validation.validation_methods import (
    get_validation_method,
)
from validation.validation_rule import (
    ClosureValidationRule,
    ConditionValidationRule,
    ValidationRule,
)


class ValidationResult:
    pass


class ValidResult(ValidationResult):
    def __init__(self, field, value) -> None:
        self.field = field
        self.value = value


class FailedResult(ValidationResult):
    def __init__(self, message) -> None:
        self.message = message


class Validator:
    def __init__(self, data: dict[str, Any], rules: dict[str, Any]) -> None:
        self._data = data
        self._rules = rules
        self._failed = None
        self._validated = {}
        self._errors = {}

    def fails(self) -> bool:
        if self._failed is None:
            try:
                self.validate()
            except ValidationError:
                pass

        return self._failed

    def validate(self):
        self._validated = {}

        for field, rules in self._rules.items():
            rules = list(filter(None, rules))

            # skip if no rules
            if len(rules) == 0:
                continue

            result = self._validate_by_rules(field, self._data.get(field), rules)

            if isinstance(result, ValidResult):
                self._validated[field] = result.value

            if isinstance(result, FailedResult):
                self._failed = True
                self._errors[field] = result.message

        self._validated = {k: v for k, v in self._validated.items() if v is not None}

        if self._failed:
            self._validated = {}
            raise ValidationError(self._errors)

        self._errors = {}

        return self._validated

    def _validate_by_rules(self, field, value, rules) -> ValidationResult:
        for rule in rules:
            if isinstance(rule, str):
                condition = get_validation_method(rule)
                validation_rule = ConditionValidationRule(condition)

            if inspect.isfunction(rule):
                validation_rule = ClosureValidationRule(rule)

            if inspect.isclass(rule) and issubclass(rule, ValidationRule):
                validation_rule = rule()

            if validation_rule is None or not isinstance(
                validation_rule, ValidationRule
            ):
                raise InvalidRuleError('Invalid rule: "{}"'.format(rule))

            if not validation_rule.passes(field, value):
                return FailedResult(validation_rule.message())

        return ValidResult(field, value)

    def validated(self):
        if self._failed is None:
            try:
                self.validate()
            except ValidationError:
                pass

        return self._validated if not self._failed else None

    def valid(self):
        if self._failed is None:
            try:
                self.validate()
            except ValidationError:
                pass

        return not self._failed

    def errors(self):
        return self._errors
