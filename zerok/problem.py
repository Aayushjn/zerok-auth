from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any


class Problem(ABC):
    @abstractmethod
    def derive_registration_parameters(
        self, username: str, password: str, **kwargs
    ) -> Iterable[Any]:
        pass

    @abstractmethod
    def derive_auth_parameters(
        self, username: str, password: str, **kwargs
    ) -> Iterable[Any]:
        pass

    @abstractmethod
    def generate_response(self, challenge: Iterable[Any]) -> Iterable[Any]:
        pass

    @abstractmethod
    def generate_challenge(self, batch_params: Iterable[Any]) -> Iterable[Any]:
        pass
