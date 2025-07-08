import unittest.mock

import pytest

from barter_app.dto import CreateAdDTO, UpdateAdDTO
from barter_app.services import AdService


@pytest.fixture
def mock_ad_repo() -> unittest.mock.Mock:
    return unittest.mock.Mock()


@pytest.fixture
def mock_exchange_repo() -> unittest.mock.Mock:
    return unittest.mock.Mock()


@pytest.fixture
def ad_service(
    mock_ad_repo: unittest.mock.Mock,
    mock_exchange_repo: unittest.mock.Mock,
) -> AdService:
    return AdService(
        ad_repo=mock_ad_repo,
        exchange_repo=mock_exchange_repo,
    )


def test_create_ad(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
) -> None:
    input_data = CreateAdDTO(
        title="Test Ad",
        description="Test Description",
        category_id=1,
        condition="new",
    )
    ad_service.create_ad(ad_in=input_data)

    mock_ad_repo.create.assert_called_once_with(ad_in=input_data)


def test_update_ad(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
) -> None:
    input_data = UpdateAdDTO(
        title="Test Ad",
        description="Test Description",
        category_id=2,
        condition="new",
    )
    ad_service.update_ad(
        ad_edit=input_data,
        ad_id=1,
    )

    mock_ad_repo.update.assert_called_once_with(
        ad_edit=input_data,
        ad_id=1,
    )


def test_get_ad_by_id(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
) -> None:
    ad_service.get_ad_by_id(ad_id=1)

    mock_ad_repo.get_by_id.assert_called_once_with(ad_id=1)


def test_get_all_ads(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
) -> None:
    ad_service.get_all_ads()

    mock_ad_repo.get_all.assert_called_once()


def test_get_filtered_ads(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
) -> None:
    ad_service.get_filtered_ads(
        search_query="test",
        category_slug="test",
        condition="new",
    )

    mock_ad_repo.get_filtered_ads.assert_called_once_with(
        search_query="test",
        category_slug="test",
        condition="new",
    )


def test_get_available_ads(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
    mock_exchange_repo: unittest.mock.Mock,
) -> None:
    mock_exchange_repo.get_sender_ids_by_receiver_id.return_value = [1, 2, 3]

    ad_service.get_available_exchange_ads(
        sender_id=1,
        receiver_id=2,
    )

    mock_exchange_repo.get_sender_ids_by_receiver_id.assert_called_once_with(
        receiver_id=2,
    )
    mock_ad_repo.get_available_ads.assert_called_once_with(
        user_id=1,
        sender_ids=[1, 2, 3],
    )


def test_delete_ad(
    ad_service: AdService,
    mock_ad_repo: unittest.mock.Mock,
) -> None:
    ad_service.delete_ad(ad_id=1)

    mock_ad_repo.delete.assert_called_once_with(ad_id=1)
