import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 200), (False, 403)]
)
@pytest.mark.django_db
def test_feed(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    page,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.get(f"/feed/", HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "is_admin, is_page_owner, is_owner_moderator, expected_status",
    [
        (False, False, False, 403),
        (True, False, False, 200),
        (False, True, False, 200),
        (False, False, True, 200),
        (True, True, False, 200),
    ],
)
@pytest.mark.django_db
def test_update_post(
    is_admin,
    is_page_owner,
    is_owner_moderator,
    expected_status,
    is_owner_or_admin_or_moderator_post_mock,
    mock_get,
    post,
):
    is_owner_or_admin_or_moderator_post_mock.return_value = (
        is_page_owner or is_admin or is_owner_moderator
    )

    new_credentials = {"content": "new_content"}

    response = client.patch(f"/post/{post.id}/", new_credentials, HTTP_token="token")

    assert response.status_code == expected_status

    if is_page_owner or is_admin or is_owner_moderator:
        assert response.json().get("content") == new_credentials.get("content")


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
def test_destroy_post(
    is_admin,
    is_page_owner,
    is_owner_moderator,
    expected_status,
    is_owner_or_admin_or_moderator_post_mock,
    mock_get,
    post,
):
    is_owner_or_admin_or_moderator_post_mock.return_value = (
        is_page_owner or is_admin or is_owner_moderator
    )

    response = client.delete(f"/post/{post.id}/", HTTP_token="token")

    assert response.status_code == expected_status
