import dataclasses


@dataclasses.dataclass
class CreateAdDTO:
    """DTO для создания нового объявления."""

    title: str
    description: str
    category_id: int
    condition: str
    user_id: int | None = None
    image_url: str | None = dataclasses.field(default="")

    def to_dict(self) -> dict:
        """Преобразует DTO в словарь для передачи в репозиторий."""
        return dataclasses.asdict(self)
