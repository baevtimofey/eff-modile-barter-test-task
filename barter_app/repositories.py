import django.db.models

from . import (
    dto,
    models,
)


class AdRepository:
    """Репозиторий для работы с объявлениями."""

    @staticmethod
    def get_all() -> django.db.models.QuerySet[models.Ad]:
        """Получает все объявления."""
        return models.Ad.objects.all()

    @staticmethod
    def create(*, ad_in: dto.CreateAdDTO) -> None:
        """Создает новое объявление."""
        models.Ad.objects.create(**ad_in.to_dict())
