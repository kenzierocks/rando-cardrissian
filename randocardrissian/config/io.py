from io import TextIOBase, StringIO
from typing import Callable
from typing import Union

from .configobj import Configuration

FileInput = Union[TextIOBase, str, bytes]


def load(f: FileInput) -> Configuration:
    if isinstance(f, str):
        return _load(StringIO(f), True)
    elif isinstance(f, bytes):
        return _load(StringIO(f.decode('utf-8')), True)
    else:
        return _load(f, False)


def _load(f: TextIOBase, close) -> Configuration:
    # here's the thing -- it's just python!
    try:
        source = f.read()
    finally:
        if close:
            f.close()

    config = Configuration()
    value_cap = ConfigHandler(config, config.is_config_value)
    # capture configuration values
    # the code should define a method called "configure"
    # that method will be called with the config obj as the only argument
    cfg_vars = {}
    exec(source, cfg_vars)

    if 'configure' not in cfg_vars:
        raise KeyError(
            "Configure code did not define a method named 'configure'")

    cfg_vars['configure'](value_cap)

    config.validate_values()

    return config


class ConfigHandler:
    _no_forward = ['_key_filter', '_cfg']
    __slots__ = _no_forward

    def __init__(self, cfg: Configuration, key_filter: Callable[[str], bool]):
        self._key_filter = key_filter
        self._cfg = cfg

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            pass
        if key in ConfigHandler._no_forward:
            raise AttributeError(key)
        return getattr(self._cfg, key)

    def __setattr__(self, key, value):
        if key in ConfigHandler._no_forward:
            object.__setattr__(self, key, value)
            return
        if not self._key_filter(key):
            raise KeyError(f"No configuration value named {key}")
        setattr(self._cfg, key, value)


__all__ = ['load']
