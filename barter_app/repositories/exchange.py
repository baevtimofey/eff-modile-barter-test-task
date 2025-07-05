import django.db.models

from barter_app import models
from barter_app.repositories import base


class ExchangeProposalRepository(base.BaseRepository[models.ExchangeProposal]):
    """Репозиторий для работы с предложениями обмена."""

    def get_sender_ids_by_receiver_id(
        self,
        *,
        receiver_id: int,
    ) -> django.db.models.QuerySet[int]:
        """Получить идентификаторы отправителей существующих предложений обмена."""
        return (
            self._model_class.objects
            .filter(ad_receiver_id=receiver_id)
            .values_list("ad_sender_id", flat=True)
        )
