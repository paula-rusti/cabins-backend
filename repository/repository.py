import abc

from models import dto_models


class AbstractCabinsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, cabin, user_id):
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
    def add(self, item: dto_models.PhotoIn):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, _id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_cabin(self, cabin_id: int):
        raise NotImplementedError


class AbstractReviewRepository(abc.ABC):
    @abc.abstractmethod
    def add_review(self, review, user_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_of_cabin(self, cabin_id, skip, limit):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_of_tourist(self, user_id, skip, limit):
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_of_booking(self, user_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self, _id):
        raise NotImplementedError
