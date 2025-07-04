import django.views.generic

from . import (
    models,
    services,
)


class AdListView(django.views.generic.ListView):
    """Контроллер для отображения списка объявлений."""

    ad_service: services.AdService = services.AdService()

    template_name = "barter_app/ad_list.html"
    context_object_name = "ads"
    paginate_by = 10

    def get_queryset(self) -> django.db.models.QuerySet[models.Ad]:
        """Получение списка объявлений."""
        return self.ad_service.get_all_ads()
