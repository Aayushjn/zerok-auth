from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any
from typing import Mapping
from typing import TypeVar


C = TypeVar("C")
R = TypeVar("R")


class Problem(ABC):
    @abstractmethod
    def derive_registration_parameters(self, username: str, password: str, **kwargs) -> Iterable[Any]:
        pass

    @abstractmethod
    def derive_auth_parameters(self, username: str, password: str, **kwargs) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def generate_responses(
        self,
        challenge: Iterable[Any],
        auth_params: Iterable[Any],
        other_params: Mapping[str, Any],
    ) -> Iterable[R]:
        pass

    @abstractmethod
    def generate_challenges(self, **kwargs) -> Iterable[C]:
        pass

    @abstractmethod
    def verify(
        self, params: Iterable[Any], responses: Iterable[Any], challenges: Iterable[int], user_params: Iterable[Any]
    ) -> bool:
        pass
