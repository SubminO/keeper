class AttrProxy:
    def __init__(self, instance, name):
        self.instance = instance
        self.name = "_" + name

    def inc(self):
        new_value = getattr(self.instance, self.name) + 1
        setattr(self.instance, self.name, new_value)
        return new_value


class A:
    def __init__(self):
        self._a = 0
        self._b = 0

    def __getattr__(self, name):
        obj = AttrProxy(self, name)
        print(id(obj))
        return obj


a = A()
a.a.inc()