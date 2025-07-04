from barter_app.repositories import base

from barter_app import (
    dto,
    exceptions,
    models,
)


class AdRepository(base.BaseRepository[models.Ad]):
    """Репозиторий для работы с объявлениями."""

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
        try:
            return models.Ad.objects.get(pk=ad_id)
        except models.Ad.DoesNotExist as err:
            raise exceptions.AdDoesNotExistError from err

    @staticmethod
    def delete(*, ad_id: int) -> None:
        """Удаляет объявление."""
        models.Ad.objects.filter(pk=ad_id).delete()
