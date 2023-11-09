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

    print(response.json())

    assert response.status_code == expected_status
