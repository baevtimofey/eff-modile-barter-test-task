import django.db.models

from barter_app import (
    dto,
    exceptions,
    models,
)
from barter_app.repositories import base


class ExchangeProposalRepository(base.BaseRepository[models.ExchangeProposal]):
    """Репозиторий для работы с предложениями обмена."""

    def get_sender_ids_by_receiver_id(
        self,
        *,
        receiver_id: int,
    ) -> django.db.models.QuerySet:
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

    def get_by_id(
        self,
        *,
        proposal_id: int,
    ) -> models.ExchangeProposal:
        """Получить предложение обмена по идентификатору."""
        try:
            return self._model_class.objects.get(id=proposal_id)
        except self._model_class.DoesNotExist as err:
            raise exceptions.ProposalDoesNotExistError from err

    def update_status(
        self,
        *,
        proposal_id: int,
        status: str,
    ) -> models.ExchangeProposal:
        """Обновить статус предложения обмена."""
        proposal = self.get_by_id(proposal_id=proposal_id)
        proposal.status = status
        proposal.save(update_fields=["status"])
        return proposal

    def reject_other_proposals(
        self,
        *,
        accepted_proposal_id: int,
        ad_ids: list[int],
    ) -> None:
        """Отклоняет все другие предложения для указанных объявлений."""
        self._model_class.objects.filter(
            ~django.db.models.Q(id=accepted_proposal_id),
            (
                django.db.models.Q(ad_sender_id__in=ad_ids)
                | django.db.models.Q(ad_receiver_id__in=ad_ids)
            ),
            status=self._model_class.Status.PENDING,
        ).update(status=self._model_class.Status.REJECTED)
