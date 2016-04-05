class TodoObj(object):
    """
    Dynamic properties for this class, according to keys from a dict.
    FROM: http://goodcode.io/articles/python-dict-object/
    """

    def __init__(self, d):
        self.__dict__ = d

    def __getattribute__(self, key):
        return object.__getattribute__(self, key)
    


class TodoContainer(object):
    def __init__(self, todosList):
        self.todos_obj = [TodoObj(x) for x in todosList]

    def getBy(self, **kw):
        for prop, value in kw.items():
            for it in self.todos_obj:
                if getattr(it, prop) == value:
                    return it
        return False

    def all(self):
        return [vars(obj) for obj in self.todos_obj]


