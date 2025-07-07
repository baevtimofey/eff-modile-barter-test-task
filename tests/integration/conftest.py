import random
from typing import Unpack

import mimesis.schema
import pytest

import barter_app.models
from tests.integration import annotations


@pytest.fixture
def category() -> barter_app.models.Category:
    mf = mimesis.schema.Field()
    return barter_app.models.Category.objects.create(
        name=mf("text.title"),
    )


@pytest.fixture
def condition() -> barter_app.models.Ad.Condition:
    return random.choice(list(barter_app.models.Ad.Condition))


@pytest.fixture
def ad_creation_data_factory(
    category: barter_app.models.Category,
    condition: barter_app.models.Ad.Condition,
) -> annotations.AdCreationDataFactory:
    """Фабрика для создания данных для создания объявления."""

    def factory(
        **fields: Unpack[annotations.AdCreationData],
    ) -> annotations.AdCreationData:
        mf = mimesis.schema.Field()
        schema = mimesis.schema.Schema(
            schema=lambda: {
                "title": mf("text.word"),
                "description": mf("text.text"),
                "image": mf("internet.url"),
            },
            iterations=1,
        )
        return {
            **schema.create()[0],  # type: ignore[typeddict-item]
            "condition": condition,
            "category": category.pk,
            **fields,
        }

    return factory


@pytest.fixture
def ad_creation_data(
    ad_creation_data_factory: annotations.AdCreationDataFactory,
) -> annotations.AdCreationData:
    """Фикстура для создания данных для создания объявления."""
    return ad_creation_data_factory()


@pytest.fixture
def ad_data(ad_creation_data: annotations.AdCreationData) -> annotations.AdData:
    result: annotations.AdData = {
        "exchanged": False,
    }
    result.update(ad_creation_data)
    return result


@pytest.fixture
def assert_correct_ad() -> annotations.AdAssertion:
    def factory(
        *,
        title: str,
        expected: annotations.AdData,
    ) -> None:
        ad = barter_app.models.Ad.objects.get(title=title)
        assert ad.created_at is not None
        assert ad.category.pk == expected.pop("category")
        for field_name, date_value in expected.items():
            assert getattr(ad, field_name) == date_value

    return factory
