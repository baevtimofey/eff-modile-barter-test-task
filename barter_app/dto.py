import dataclasses


@dataclasses.dataclass
class BaseAdDTO:
    """Базовый DTO для объявлений."""

    title: str
    description: str
    category_id: int
    condition: str
    user_id: int | None = None
    image_url: str | None = dataclasses.field(default="")

    def to_dict(self) -> dict:
        """Преобразует DTO в словарь для передачи в репозиторий."""
        return dataclasses.asdict(self)


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
