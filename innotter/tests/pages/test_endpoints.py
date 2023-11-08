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
    user_credentials,
    tag,
):
    is_authenticated_mock.return_value = is_authenticated

    response = client.post("/page/", page_credentials, HTTP_token="ffff")

    assert response.status_code == expected_status
