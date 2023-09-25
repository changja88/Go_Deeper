class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print(meta)
        print(name)
        print(bases)
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)


class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        ...
