import dataclasses

import django.core.files.base


@dataclasses.dataclass
class BaseAdDTO:
    """Базовый DTO для объявлений."""

    title: str
    description: str
    category_id: int
    condition: str
    user_id: int | None = None
    image: django.core.files.base.File | None = dataclasses.field(default=None)

    def to_dict(self) -> dict:
        """Преобразует DTO в словарь для передачи в репозиторий."""
        return {
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "condition": self.condition,
            "user_id": self.user_id,
            "image": self.image,
        }


@dataclasses.dataclass
class CreateAdDTO(BaseAdDTO):
    """DTO для создания нового объявления."""


@dataclasses.dataclass
class UpdateAdDTO(BaseAdDTO):
    """DTO для обновления объявления."""


@dataclasses.dataclass
class ExchangeProposalDTO:
    """DTO для предложения обмена."""

    ad_sender_id: int
    ad_receiver_id: int
    comment: str = dataclasses.field(default="")

    def to_dict(self) -> dict:
        """Преобразует DTO в словарь для передачи в репозиторий."""
        return dataclasses.asdict(self)
