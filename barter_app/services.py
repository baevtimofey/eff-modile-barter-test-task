import django.db.models

from . import (
    dto,
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

    def create_ad(
        self,
        *,
        ad_in: dto.CreateAdDTO,
    ) -> None:
        """Создает новое объявление."""
        self._repo.create(ad_in=ad_in)
