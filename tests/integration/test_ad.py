import http

import django.http
import django.test
import django.urls
import pytest

from tests.integration import annotations


@pytest.mark.django_db
def test_valid_ad_create(
    client: django.test.Client,
    ad_creation_data: annotations.AdCreationData,
    ad_data: annotations.AdData,
    assert_correct_ad: annotations.AdAssertion,
) -> None:
    response = client.post(
        path=django.urls.reverse("barter_app:ad_create"),
        data=ad_creation_data,
    )

    assert response.status_code == http.HTTPStatus.FOUND
    assert_correct_ad(
        title=ad_creation_data["title"],
        expected=ad_data,
    )
