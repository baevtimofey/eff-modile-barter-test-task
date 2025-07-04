import django.db.models

from . import (
    dto,
    models,
)
from .repositories import (
    ad,
    category,
)


class AdService:
    """Сервис для бизнес-логики, связанной с объявлениями."""

    def __init__(self) -> None:
        self._repo: ad.AdRepository = ad.AdRepository(
            model_class=models.Ad,
        )

    def get_all_ads(self) -> django.db.models.QuerySet[models.Ad]:
        """Получает все объявления."""
        return self._repo.get_all()
    
    def get_filtered_ads(
        self,
        *,
        search_query: str | None = None,
        category_slug: str | None = None,
        condition: str | None = None,
    ) -> django.db.models.QuerySet[models.Ad]:
        """Получает отфильтрованный список объявлений."""
        return self._repo.get_filtered_ads(
            search_query=search_query,
            category_slug=category_slug,
            condition=condition,
        )

    def create_ad(
        self,
        *,
        ad_in: dto.CreateAdDTO,
    ) -> None:
        """Создает новое объявление."""
        self._repo.create(ad_in=ad_in)

    def update_ad(
        self,
        *,
        ad_edit: dto.UpdateAdDTO,
        ad_id: int,
    ) -> None:
        """Обновляет объявление."""
        self._repo.update(
            ad_edit=ad_edit,
            ad_id=ad_id,
        )

    def get_ad_by_id(
        self,
        *,
        ad_id: int,
    ) -> models.Ad:
        """Получает объявление по ID."""
        return self._repo.get_by_id(ad_id=ad_id)

    def delete_ad(self, *, ad_id: int) -> None:
        """Удаляет объявление."""
        self._repo.delete(ad_id=ad_id)


class CategoryService:
    """Сервис для бизнес-логики, связанной с категориями."""

    def __init__(self) -> None:
        self._repo: category.CategoryRepository = category.CategoryRepository(
            model_class=models.Category,
        )

    def get_all_categories(self) -> django.db.models.QuerySet[models.Category]:
        """Получает все категории."""
        return self._repo.get_all()
