import inspect


def make_dependencies_lazy(service_class):
    '''
    Make all dependencies (instance of `Dependency`) defined in `service_class`
    initialize lazily
    '''
    dependencies = inspect.getmembers(service_class, is_dependency)
    for name, dependency in dependencies:
        setattr(service_class, name, LazyInitialized(name, dependency))


class LazyInitialized(object):
    '''
    Descriptor that on get replaces itself by an initialised dependency
    '''

    def __init__(self, name, dependency):
        self.dependency = dependency
        self.name = name

    def __get__(self, instance, cls):
        self.dependency.initialize()
        setattr(cls, self.name, self.dependency)
        return self.dependency


def is_dependency(attribute):
    return isinstance(attribute, Dependency)


class Dependency(object):
    def initialize(self):
        raise NotImplemented
