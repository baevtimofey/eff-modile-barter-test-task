from barter_app.repositories import base

from barter_app import models


class CategoryRepository(base.BaseRepository[models.Category]):
    """Репозиторий для работы с категориями."""
