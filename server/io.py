class IO():
    def __init__(self, type, format, name, group, ioa):
        self.type = type
        self.format = format
        self.name = name
        self.group = group
        self.ioa = ioa
        self.value = None
        self.timestamp = None
        self.quality = None

    def validate(self):
        return self.type is not None\
            and self.format is not None\
            and self.ioa is not None\
            and self.name is not None\
            and self.group is not None\
            and self.ioa is not None


class IOStorage():

    def __init__(self):
        self._db = dict()

    def insert(self, tag):
        name = tag.name
        if name not in self._db:
            self._db[name] = tag
            return True
        return False

    def update(self, tag):
        print("Update value --", tag.value)
        name = tag.name
        if name in self._db:
            self._db[name] = tag
            return True

        return False

    def get(self, name):
        if name in self._db:
            return self._db[name]
        return IO(None, None)

    def record(self, name):
        return self._db[name]

    def items(self):
        return self._db.items()

    def keys(self):
        return self._db.keys()

    def values(self):
        return self._db.values()

    @property
    def count(self):
        return len(self._db.keys())
