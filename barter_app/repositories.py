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

    @staticmethod
    def update(
        *,
        ad_edit: dto.UpdateAdDTO,
        ad_id: int,
    ) -> None:
        """Обновляет объявление."""
        update_data = ad_edit.to_dict()
        models.Ad.objects.filter(pk=ad_id).update(**update_data)

    @staticmethod
    def get_by_id(*, ad_id: int) -> models.Ad:
        """Получает объявление по ID."""
        return models.Ad.objects.get(pk=ad_id)
