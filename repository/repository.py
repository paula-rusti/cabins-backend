import abc


class AbstractCabinsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item):
        raise NotImplementedError

    # @abc.abstractmethod
    # def get(self, reference):
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, skip: int, limit: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_count(self):
        raise NotImplementedError


class AbstractPhotoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item):
        raise NotImplementedError
