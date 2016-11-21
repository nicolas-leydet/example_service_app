# Idea
# dependency with lazy initialisation, optionally pooled
# replaceable for testing without mock

from collections import deque


class PooledServiceDependency(object):

    def __init__(self, size=100):
        self.pool = deque(maxlen=size)

    def create_dependency(self):
        pass

    def get_dependency(self):
        try:
            self.pool.pop()
        except IndexError:
            pass

    def release_dependency(self, dependency):
        pass

    def destroy_dependency(self, dependency):
        pass

    def __get__(self, instance, cls):
        try:
            return self._instance
        except AttributeError:
            self.setup()
            self._instance = self
            return self

    def terminate():
        raise NotImplemented()
