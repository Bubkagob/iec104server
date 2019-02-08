from typing import Dict


class IO():
    def __init__(self, ioa, type, name, group):
        self.ioa = ioa
        self.type = type
        self.name = name
        self.group = group
        self.value = None
        self.timestamp = None
        self.quality = None

    def validate(self):
        return self.ioa is not None\
            and self.type is not None\
            and self.name is not None\
            and self.group is not None


class IOPool():
    def __init__(self):
        self._db: Dict[int, IO] = dict()

    def add(self, io):
        if io.ioa not in self._db:
            self._db[io.ioa] = io
            return True
        return False

    def get(self, name):
        if name in self._db:
            return self._db[name]
        return IO(None, None, None, None)

    def get_io_by_name(self, name):
        if name in self.subscribe_list():
            return next(el for el in self.get_measures() if el.name == name)
            # return self._db[name]
        return IO(None, None, None, None)

    def get_io_by_addr(self, ioa):
        if ioa in self.ioaddresses():
            return next(el for el in self.values() if el.ioa == ioa)
            # return self._db[name]
        return IO(None, None, None, None)

    def update(self, io):
        if io.ioa in self._db:
            self._db[io.ioa] = io
            return True
        return False

    @property
    def count(self):
        return len(self._db.keys())

    def items(self):
        return self._db.items()

    def keys(self):
        return self._db.keys()

    def ioaddresses(self):
        return list(self._db.keys())

    def values(self):
        return self._db.values()

    def subscribe_list(self):
        return [io.name for io in self._db.values() if io.type in range(1, 40)]

    def get_commands(self):
        return [io for io in self._db.values() if io.type in range(45, 107)]

    def get_measures(self):
        return [io for io in self._db.values() if io.type in range(1, 40)]
