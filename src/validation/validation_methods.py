from validation.errors import InvalidRuleError


def get_validation_method(rule: str):
    try:
        return getattr(_ValidationMethods, f"validate_{rule}")
    except AttributeError:
        raise InvalidRuleError(f"Validation rule {rule} does not exist")


class _ValidationMethods:
    @staticmethod
    def validate_string(value) -> bool:
        return isinstance(value, str)

    @staticmethod
    def validate_required(value) -> bool:
        return value is not None

    @staticmethod
    def validate_integer(value) -> bool:
        if not isinstance(value, int):
            try:
                int(value)
            except ValueError:
                return False

        return True
