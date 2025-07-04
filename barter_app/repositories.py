import django.db.models

from . import models


class AdRepository:
    """Репозиторий для работы с объявлениями."""

    @staticmethod
    def get_all() -> django.db.models.QuerySet[models.Ad]:
        """Получает все объявления."""
        return models.Ad.objects.all()
