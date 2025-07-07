import django.test
import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup() -> None:
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db.sqlite3",
        "ATOMIC_REQUESTS": False,
    }


@pytest.fixture
def client(
    django_user_model: django.contrib.auth.models.User,
) -> django.test.Client:
    username = "testuser"
    password = "testpass123"
    django_user_model.objects.create_user(
        username=username,
        password=password,
    )

    client = django.test.Client()
    client.login(
        username=username,
        password=password,
    )

    return client
