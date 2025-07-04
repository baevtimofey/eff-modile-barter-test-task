import django.contrib.auth.mixins
import django.contrib.messages
import django.db.models
import django.http
import django.urls
import django.views.generic
from django.utils.translation import gettext_lazy as _

from . import (
    exceptions,
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


class AdUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.UpdateView,
):
    """Контроллер для обновления объявления."""

    ad_service: services.AdService = services.AdService()

    form_class = forms.AdForm
    template_name = "barter_app/ad_form.html"
    success_url = django.urls.reverse_lazy("barter_app:ad_list")

    def get_object(self) -> models.Ad:
        try:
            return self.ad_service.get_ad_by_id(ad_id=self.kwargs["pk"])
        except exceptions.AdDoesNotExistError as err:
            raise django.http.Http404 from err

    def test_func(self) -> bool:
        return self.get_object().user == self.request.user

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: forms.AdForm) -> django.http.HttpResponseRedirect:
        ad_edit = form.get_data()
        self.ad_service.update_ad(
            ad_edit=ad_edit,
            ad_id=self.kwargs["pk"],
        )
        django.contrib.messages.success(
            self.request,
            _("Объявление успешно обновлено."),
        )
        return django.http.HttpResponseRedirect(redirect_to=self.success_url)


class AdDeleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.DeleteView,
):
    """Контроллер для удаления объявления."""

    ad_service: services.AdService = services.AdService()

    template_name = "barter_app/ad_confirm_delete.html"
    success_url = django.urls.reverse_lazy("barter_app:ad_list")

    def get_object(self) -> models.Ad:
        try:
            return self.ad_service.get_ad_by_id(ad_id=self.kwargs["pk"])
        except exceptions.AdDoesNotExistError as err:
            raise django.http.Http404 from err

    def test_func(self) -> bool:
        return self.get_object().user == self.request.user

    def delete(self) -> django.http.HttpResponseRedirect:
        self.ad_service.delete_ad(ad_id=self.kwargs["pk"])
        return django.http.HttpResponseRedirect(redirect_to=self.success_url)


class AdDetailView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.DetailView,
):
    """Контроллер для отображения деталей объявления."""

    ad_service: services.AdService = services.AdService()

    template_name = "barter_app/ad_detail.html"
    context_object_name = "ad"

    def get_object(self) -> models.Ad:
        try:
            return self.ad_service.get_ad_by_id(ad_id=self.kwargs["pk"])
        except exceptions.AdDoesNotExistError as err:
            raise django.http.Http404 from err
