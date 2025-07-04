import django.db.models

from barter_app import (
    dto,
    exceptions,
    models,
)
from barter_app.repositories import base


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
    def get_filtered_ads(
        *,
        search_query: str | None = None,
        category_slug: str | None = None,
        condition: str | None = None,
    ) -> django.db.models.QuerySet[models.Ad]:
        """Получает отфильтрованный список объявлений."""
        queryset = models.Ad.objects.all()
        if search_query:
            queryset = queryset.filter(
                django.db.models.Q(title__icontains=search_query)
                | django.db.models.Q(description__icontains=search_query)
            )
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if condition:
            queryset = queryset.filter(condition=condition)
            
        return queryset

    @staticmethod
    def delete(*, ad_id: int) -> None:
        """Удаляет объявление."""
        models.Ad.objects.filter(pk=ad_id).delete()
