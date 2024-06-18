from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def save(self, data):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError
