from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any
from typing import Mapping


class Problem(ABC):
    @abstractmethod
    def derive_registration_parameters(
        self, username: str, password: str, **kwargs
    ) -> Iterable[Any]:
        pass

    @abstractmethod
    def derive_auth_parameters(
        self, username: str, password: str, **kwargs
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def generate_responses(
        self,
        challenge: Iterable[Any],
        auth_params: Iterable[Any],
        other_params: Iterable[Any],
    ) -> Iterable[Any]:
        pass

    @abstractmethod
    def generate_challenge(self, batch_params: Iterable[Any]) -> Iterable[Any]:
        pass
