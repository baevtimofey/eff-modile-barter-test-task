from collections.abc import Callable
from typing import Protocol, TypedDict, Unpack, final

import mypy_extensions


class AdCreationData(TypedDict, total=False):
    """Данные для создания объявления."""

    title: str
    description: str
    image_url: str
    category: int
    condition: str


@final
class AdData(AdCreationData, total=False):
    """Данные созданного объявления."""

    exchanged: bool


class AdCreationDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[AdCreationData],
    ) -> AdCreationData:
        """Фабрика для создания данных для создания объявления протокол."""
        ...


type AdAssertion = Callable[
    [
        mypy_extensions.NamedArg(str, "title"),
        mypy_extensions.NamedArg(AdData, "expected"),
    ],
    None,
]
