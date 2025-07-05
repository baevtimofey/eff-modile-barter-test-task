from typing import ParamSpec

import django.forms
from django.utils.translation import gettext_lazy as _

from . import (
    dto,
    models,
)

P = ParamSpec("P")


class AdForm(django.forms.ModelForm):
    """Форма для создания и редактирования объявлений."""

    class Meta:
        model = models.Ad
        fields = ["title", "description", "image_url", "category", "condition"]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["title"].help_text = _("Указывайте краткое и точное название")
        self.fields["description"].help_text = _(
            "Укажите состояние, особенности и причину обмена"
        )
        self.fields["image_url"].help_text = _("Ссылка на изображение товара")

    def get_data(self) -> dto.CreateAdDTO:
        return dto.CreateAdDTO(
            title=self.cleaned_data["title"],
            description=self.cleaned_data["description"],
            category_id=self.cleaned_data["category"].id,
            condition=self.cleaned_data["condition"],
            user_id=self.user.id,
            image_url=self.cleaned_data["image_url"],
        )


class ExchangeProposalForm(django.forms.ModelForm):
    """Форма для создания предложения обмена."""

    class Meta:
        model = models.ExchangeProposal
        fields = ["comment", "ad_sender"]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        exchange_ads = kwargs.pop("exchange_ads", None)
        self.ad_receiver_id = kwargs.pop("ad_receiver_id", None)
        super().__init__(*args, **kwargs)
        if exchange_ads is not None:
            self.fields["ad_sender"].queryset = exchange_ads

    def get_data(self) -> dto.ExchangeProposalDTO:
        return dto.ExchangeProposalDTO(
            ad_sender_id=self.cleaned_data["ad_sender"].id,
            ad_receiver_id=self.ad_receiver_id,
            comment=self.cleaned_data["comment"],
        )
