import django.contrib.auth.mixins
import django.contrib.messages
import django.db.models
import django.http
import django.urls
import django.views.generic
from django.utils.translation import gettext_lazy as _

from . import (
    forms,
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


class AdCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    """Контроллер для создания нового объявления."""

    ad_service: services.AdService = services.AdService()

    form_class = forms.AdForm
    template_name = "barter_app/ad_form.html"
    success_url = django.urls.reverse_lazy("barter_app:ad_list")

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: forms.AdForm) -> django.http.HttpResponseRedirect:
        ad_in = form.get_data()
        self.ad_service.create_ad(ad_in=ad_in)
        django.contrib.messages.success(
            self.request,
            _("Объявление успешно создано."),
        )
        return django.http.HttpResponseRedirect(redirect_to=self.success_url)
