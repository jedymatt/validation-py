import abc

from validation.rules import Rules


class Rule(abc.ABC):
    @abc.abstractmethod
    def passes(self, field, value) -> bool:
        pass

    @abc.abstractmethod
    def message(self) -> str:
        pass


class Validator(abc.ABC):
    _rules: dict

    size_rules = [Rules.min]
    numeric_rules = [Rules.integer]

    def has_rule(self, field, rule) -> bool:
        return field in self._rules and rule in self._rules[field]

    def has_numeric_rules(self, field) -> bool:
        if field not in self._rules:
            return False

        return any([rule in self._rules[field] for rule in self.numeric_rules])

    def has_size_rules(self, field) -> bool:
        if field not in self._rules:
            return False

        return any([rule in self._rules[field] for rule in self.size_rules])

    def get_field_type(self, field) -> str:
        if self.has_numeric_rules(field):
            return "numeric"

        return "string"

    @abc.abstractmethod
    def validate():
        pass

    @abc.abstractmethod
    def fails():
        pass

    # @abc.abstractmethod
    def passes() -> bool:
        #  TODO: implement passes method
        pass