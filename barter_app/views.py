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
    category_service: services.CategoryService = services.CategoryService()

    template_name = "barter_app/ad_list.html"
    context_object_name = "ads"
    paginate_by = 10

    def get_queryset(self) -> django.db.models.QuerySet:
        """Получение отфильтрованного списка объявлений."""
        return self.ad_service.get_filtered_ads(
            search_query=self.request.GET.get("q"),
            category_slug=self.request.GET.get("category"),
            condition=self.request.GET.get("condition"),
        )

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["categories"] = self.category_service.get_all_categories()
        context["q"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_condition"] = self.request.GET.get("condition", "")
        context["condition_choices"] = models.Ad.Condition.choices
        return context


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

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        if (sender := self.request.user) != (receiver := self.object.user):
            exchange_ads = self.ad_service.get_available_exchange_ads(
                sender_id=sender.id,
                receiver_id=receiver.id,
            )
            context["exchange_form"] = forms.ExchangeProposalForm(
                exchange_ads=exchange_ads,
            )
        return context


class ExchangeProposalCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    """Контроллер для создания предложения обмена."""

    ad_service: services.AdService = services.AdService()
    exchange_service: services.ExchangeProposalService = (
        services.ExchangeProposalService()
    )

    form_class = forms.ExchangeProposalForm
    template_name = "barter_app/exchange_proposal_form.html"
    success_url = django.urls.reverse_lazy("barter_app:ad_list")

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["ad_receiver_id"] = self.kwargs.get("ad_id")
        return kwargs

    def form_valid(
        self,
        form: forms.ExchangeProposalForm,
    ) -> django.http.HttpResponseRedirect:
        proposal_in = form.get_data()
        self.exchange_service.create_proposal(proposal_in=proposal_in)
        django.contrib.messages.success(
            self.request,
            _("Предложение обмена успешно отправлено."),
        )
        return django.http.HttpResponseRedirect(redirect_to=self.success_url)


class ProposalsListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    """Контроллер для отображения списка предложений пользователя."""

    template_name = "barter_app/proposals.html"
    context_object_name = "proposals"
    exchange_service: services.ExchangeProposalService = (
        services.ExchangeProposalService()
    )

    def get_queryset(self) -> django.db.models.QuerySet[models.ExchangeProposal]:
        proposal_type = self.request.GET.get("type", "sent")
        if proposal_type == "received":
            return self.exchange_service.get_received_proposals(
                user_id=self.request.user.id,
            )
        return self.exchange_service.get_sent_proposals(
            user_id=self.request.user.id,
        )


class ExchangeProposalDetailView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.DetailView,
):
    """Контроллер для отображения деталей предложения обмена."""

    template_name = "barter_app/exchange_proposal_detail.html"
    context_object_name = "proposal"
    exchange_service: services.ExchangeProposalService = (
        services.ExchangeProposalService()
    )

    def get_object(self) -> None:
        try:
            proposal = self.exchange_service.get_proposal_by_id(
                proposal_id=self.kwargs["pk"]
            )
        except exceptions.DoesNotExistError as err:
            raise django.http.Http404 from err
        else:
            return proposal

    def test_func(self) -> bool:
        return (
            self.get_object().ad_sender.user == self.request.user
            or self.get_object().ad_receiver.user == self.request.user
        )
