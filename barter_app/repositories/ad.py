import django.db.models

from barter_app import (
    dto,
    exceptions,
    models,
)
from barter_app.repositories import base


class AdRepository(base.BaseRepository[models.Ad]):
    """Репозиторий для работы с объявлениями."""

    def create(
        self,
        *,
        ad_in: dto.CreateAdDTO,
    ) -> None:
        """Создает новое объявление."""
        self._model_class.objects.create(**ad_in.to_dict())

    def update(
        self,
        *,
        ad_edit: dto.UpdateAdDTO,
        ad_id: int,
    ) -> None:
        """Обновляет объявление."""
        update_data = ad_edit.to_dict()
        self._model_class.objects.filter(pk=ad_id).update(**update_data)

    def get_by_id(
        self,
        *,
        ad_id: int,
    ) -> models.Ad:
        """Получает объявление по ID."""
        try:
            return self._model_class.objects.get(pk=ad_id)
        except self._model_class.DoesNotExist as err:
            raise exceptions.AdDoesNotExistError from err

    def get_filtered_ads(
        self,
        *,
        search_query: str | None = None,
        category_slug: str | None = None,
        condition: str | None = None,
    ) -> django.db.models.QuerySet[models.Ad]:
        """Получает отфильтрованный список объявлений."""
        queryset = self._model_class.objects.all()
        if search_query:
            queryset = queryset.filter(
                django.db.models.Q(title__icontains=search_query)
                | django.db.models.Q(description__icontains=search_query)
            )
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.filter(exchanged=False)

    def get_available_ads(
        self,
        *,
        user_id: int,
        sender_ids: django.db.models.QuerySet[int],  # type: ignore [type-var]
    ) -> django.db.models.QuerySet[models.Ad]:
        """Получает доступные объявления для обмена."""
        return self._model_class.objects.filter(user_id=user_id).exclude(
            id__in=sender_ids
        )

    def delete(
        self,
        *,
        ad_id: int,
    ) -> None:
        """Удаляет объявление."""
        self._model_class.objects.filter(pk=ad_id).delete()

    def mark_as_exchanged(
        self,
        *,
        ad_id: int,
    ) -> None:
        """Помечает объявление как обменянное."""
        self._model_class.objects.filter(pk=ad_id).update(exchanged=True)
