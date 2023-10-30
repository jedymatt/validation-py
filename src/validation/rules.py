from typing import Iterable


# a function wrapper that identifies that this is a validation rule
def conditional_rule(rule, name=None):
    def wrapper(*args, **kwargs):
        return rule(*args, **kwargs)

    wrapper.__is_conditional_rule__ = True
    wrapper.__name__ = name or rule.__name__

    return wrapper


def is_conditional_rule(rule):
    return hasattr(rule, "__is_conditional_rule__") and rule.__is_conditional_rule__


def rule_name(rule) -> str:
    if not is_conditional_rule(rule):
        raise ValueError("The rule must be a conditional rule.")

    return rule.__name__


def require_params_length(length: int, params: tuple, rule: str):
    if len(params) < length:
        raise ValueError(f"The {rule} rule requires at least {length} parameters.")


class Rules:
    @staticmethod
    @conditional_rule
    def string(field, value) -> bool:
        return isinstance(value, str)

    @staticmethod
    @conditional_rule
    def integer(field, value) -> bool:
        return isinstance(value, int)

    @staticmethod
    @conditional_rule
    def required(field, value) -> bool:
        return value is not None

    @staticmethod
    @conditional_rule
    def min(field, value, *parameters) -> bool:
        """
        The field under validation must have a minimum value.
        """
        require_params_length(1, parameters, "min")

        if isinstance(value, str):
            return len(value.strip()) >= parameters[0]

        if isinstance(value, Iterable):
            return len(value) >= parameters[0]

        return value >= parameters[0]
