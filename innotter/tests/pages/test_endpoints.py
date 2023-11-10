import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 201), (False, 403)]
)
@pytest.mark.django_db
def test_create_page(
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
def test_retrieve_page(
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
def test_update_page(
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

    if is_pageowner:
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
def test_destroy_page(
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


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 201), (False, 403)]
)
@pytest.mark.django_db
def test_follow_page(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    page,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.patch(f"/page/{page.id}/follow/", HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 204), (False, 403)]
)
@pytest.mark.django_db
def test_unfollow_page(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    follower,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.patch(f"/page/{follower.page.id}/unfollow/", HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "is_admin, is_owner_moderator, expected_status",
    [
        (False, False, 403),
        (True, False, 200),
        (False, True, 200),
        (True, True, 200),
    ],
)
@pytest.mark.django_db
def test_block_page(
    is_admin,
    is_owner_moderator,
    expected_status,
    is_admin_or_owner_moderator_mock,
    mock_get,
    page,
):
    is_admin_or_owner_moderator_mock.return_value = is_admin or is_owner_moderator

    response = client.patch(f"/page/{page.id}/block/", HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize("is_pageowner, expected_status", [(True, 201), (False, 403)])
@pytest.mark.django_db
def test_create_page_post(
    is_pageowner, expected_status, is_page_owner_mock, mock_get, page, post_credentials
):
    is_page_owner_mock.return_value = is_pageowner

    response = client.post(
        f"/page/{page.id}/post/", post_credentials, HTTP_token="token"
    )

    assert response.status_code == expected_status

    if is_pageowner:
        assert response.json().get("content") == post_credentials.get("content")
