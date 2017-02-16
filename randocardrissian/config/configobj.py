from typing import Dict, Iterator


class ConfigValue:
    def __init__(self, default=None):
        self.default = default
        self.name = None
        self.attr_name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        attr = getattr(instance, self.attr_name, self.default)
        if attr is None:
            raise ValueError(f"No value is defined for {self.name}")
        return attr

    def __set__(self, instance, value):
        setattr(instance, self.attr_name, value)

    def __set_name__(self, owner, name):
        self.name = name
        self.attr_name = '_' + name


class Configuration:
    # ConfigValue setup

    client_id = ConfigValue()
    client_secret = ConfigValue()

    @staticmethod
    def is_config_value(x):
        return isinstance(getattr(Configuration, x, None), ConfigValue)

    def __init__(self):
        pass

    def _config_keys(self) -> Iterator[str]:
        for k in dir(self):
            if self.is_config_value(k):
                yield k

    def validate_values(self):
        for k in self._config_keys():
            getattr(self, k)

    def get_values(self) -> Dict:
        return {k: getattr(self, k) for k in self._config_keys()}

    def __repr__(self):
        return type(self).__name__ + '(' + ',\n'.join(
            '='.join(map(str, t)) for t in self.get_values().items()
        ) + ')'


__all__ = ['Configuration', 'ConfigValue']
