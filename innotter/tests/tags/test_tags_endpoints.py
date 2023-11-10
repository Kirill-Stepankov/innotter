import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 201), (False, 403)]
)
@pytest.mark.django_db
def test_create_tag(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    tag_credentials,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.post("/tag/", tag_credentials, HTTP_token="token")

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "is_authenticated, expected_status", [(True, 200), (False, 403)]
)
@pytest.mark.django_db
def test_get_tags(
    is_authenticated,
    expected_status,
    is_authenticated_mock,
    mock_get,
    tag,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.get("/tag/", HTTP_token="token")

    assert response.status_code == expected_status
