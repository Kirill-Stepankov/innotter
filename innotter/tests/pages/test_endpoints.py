import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 201), (False, 403)]
)
@pytest.mark.django_db
def test_create_task(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    page_credentials,
    tag,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.post("/page/", page_credentials, HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 200), (False, 403)]
)
@pytest.mark.django_db
def test_retrieve_task(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    page,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.get(f"/page/{page.id}/", HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize("is_pageowner, expected_status", [(True, 200), (False, 403)])
@pytest.mark.django_db
def test_update_task(
    is_pageowner,
    expected_status,
    is_page_owner_mock,
    mock_get,
    page,
):
    is_page_owner_mock.return_value = is_pageowner

    new_credentials = {"name": "newname", "description": "newdesc"}

    response = client.patch(f"/page/{page.id}/", new_credentials, HTTP_token="token")

    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json().get("name") == new_credentials.get("name")


@pytest.mark.parametrize(
    "is_admin, is_page_owner, is_owner_moderator, expected_status",
    [
        (False, False, False, 403),
        (True, False, False, 204),
        (False, True, False, 204),
        (False, False, True, 204),
        (True, True, False, 204),
    ],
)
@pytest.mark.django_db
def test_destroy_task(
    is_admin,
    is_page_owner,
    is_owner_moderator,
    expected_status,
    is_owner_or_admin_or_moderator_mock,
    mock_get,
    page,
):
    is_owner_or_admin_or_moderator_mock.return_value = (
        is_page_owner or is_admin or is_owner_moderator
    )

    response = client.delete(f"/page/{page.id}/", HTTP_token="token")

    assert response.status_code == expected_status
