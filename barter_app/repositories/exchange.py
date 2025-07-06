import django.db.models

from barter_app import (
    dto,
    models,
)
from barter_app.repositories import base


class ExchangeProposalRepository(base.BaseRepository[models.ExchangeProposal]):
    """Репозиторий для работы с предложениями обмена."""

    def get_sender_ids_by_receiver_id(
        self,
        *,
        receiver_id: int,
    ) -> django.db.models.QuerySet[int]:
        """Получить идентификаторы отправителей существующих предложений обмена."""
        return self._model_class.objects.filter(ad_receiver_id=receiver_id).values_list(
            "ad_sender_id", flat=True
        )

    def create(
        self,
        *,
        proposal_in: dto.ExchangeProposalDTO,
    ) -> models.ExchangeProposal:
        """Создать новое предложение обмена."""
        return self._model_class.objects.create(**proposal_in.to_dict())

    def get_sent_proposals(
        self,
        *,
        user_id: int,
    ) -> django.db.models.QuerySet:
        """Получить все отправленные предложения пользователя."""
        return self._model_class.objects.filter(
            ad_sender__user_id=user_id
        ).select_related("ad_sender", "ad_receiver")

    def get_received_proposals(
        self,
        *,
        user_id: int,
    ) -> django.db.models.QuerySet:
        """Получить все полученные предложения пользователя."""
        return self._model_class.objects.filter(
            ad_receiver__user_id=user_id
        ).select_related("ad_sender", "ad_receiver")
