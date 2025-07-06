import django.db.models

from . import (
    dto,
    models,
)
from .repositories import (
    ad,
    category,
    exchange,
)


class AdService:
    """Сервис для бизнес-логики, связанной с объявлениями."""

    def __init__(self) -> None:
        self._repo: ad.AdRepository = ad.AdRepository(
            model_class=models.Ad,
        )
        self._exchange_repo: exchange.ExchangeProposalRepository = (
            exchange.ExchangeProposalRepository(
                model_class=models.ExchangeProposal,
            )
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

    def get_available_exchange_ads(
        self,
        *,
        sender_id: int,
        receiver_id: int,
    ) -> django.db.models.QuerySet[models.Ad]:
        """
        Получает все доступные объявления для обмена.

        Исключает объявления, которые уже участвуют в текущем обмене.
        """
        sender_ids = self._exchange_repo.get_sender_ids_by_receiver_id(
            receiver_id=receiver_id,
        )
        return self._repo.get_available_ads(
            user_id=sender_id,
            sender_ids=sender_ids,
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


class ExchangeProposalService:
    """Сервис для бизнес-логики, связанной с предложениями обмена."""

    def __init__(self) -> None:
        self._repo: exchange.ExchangeProposalRepository = (
            exchange.ExchangeProposalRepository(
                model_class=models.ExchangeProposal,
            )
        )
        self._ad_repo: ad.AdRepository = ad.AdRepository(
            model_class=models.Ad,
        )

    def create_proposal(
        self,
        *,
        proposal_in: dto.ExchangeProposalDTO,
    ) -> models.ExchangeProposal:
        """Создает новое предложение обмена."""
        self._ad_repo.get_by_id(ad_id=proposal_in.ad_sender_id)
        self._ad_repo.get_by_id(ad_id=proposal_in.ad_receiver_id)
        return self._repo.create(proposal_in=proposal_in)

    def get_sent_proposals(
        self,
        *,
        user_id: int,
    ) -> django.db.models.QuerySet[models.ExchangeProposal]:
        """Получает все отправленные предложения пользователя."""
        return self._repo.get_sent_proposals(user_id=user_id)

    def get_received_proposals(
        self,
        *,
        user_id: int,
    ) -> django.db.models.QuerySet[models.ExchangeProposal]:
        """Получает все полученные предложения пользователя."""
        return self._repo.get_received_proposals(user_id=user_id)
