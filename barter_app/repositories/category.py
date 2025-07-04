from barter_app import models
from barter_app.repositories import base


class CategoryRepository(base.BaseRepository[models.Category]):
    """Репозиторий для работы с категориями."""
