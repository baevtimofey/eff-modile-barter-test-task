import django.db.models

from . import (
    models,
    repositories,
)


class AdService:
    """Сервис для бизнес-логики, связанной с объявлениями."""

    def __init__(self) -> None:
        self._repo: repositories.AdRepository = repositories.AdRepository()

    def get_all_ads(self) -> django.db.models.QuerySet[models.Ad]:
        """Получает все объявления."""
        return self._repo.get_all()
