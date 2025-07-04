from typing import TypeVar

import django.db.models

T = TypeVar("T", bound=django.db.models.Model)


class BaseRepository[T]:
    """Базовый репозиторий."""

    def __init__(
        self,
        *,
        model_class: type[T],
    ) -> None:
        self._model_class = model_class

    def get_all(self) -> django.db.models.QuerySet[T]:
        """Получает все объекты."""
        return self._model_class.objects.all()
