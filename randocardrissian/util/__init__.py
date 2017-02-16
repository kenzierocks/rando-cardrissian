


class DoubleDict(dict):
    def __init__(self, dict1, **kwargs):
        super().__init__(**kwargs)
        self._dict = dict1

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self._dict:
            self._dict[key] = value
