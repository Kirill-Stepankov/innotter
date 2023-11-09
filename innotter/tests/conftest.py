import pytest
import requests
from page.permissions import IsAuthenticated
from tag.models import Tag


@pytest.fixture
def is_authenticated_mock(mocker):
    mock = mocker.patch.object(IsAuthenticated, "has_permission")
    return mock


@pytest.fixture
def user_credentials():
    return {
        "username": "string",
        "uuid": "26b92df7-c54e-463a-9e4e-af8fe1f94088",
        "role": "User",
        "group_id": 1,
    }


@pytest.fixture
def page_credentials():
    return {"name": "pagetest", "description": "testdesc", "tags": 1}


@pytest.fixture
def mock_get(mocker, user_credentials):
    mock_response = mocker.Mock()
    mock_response.json.return_value = user_credentials
    mock_response.status_code = 200
    return mocker.patch("requests.get", return_value=mock_response)


@pytest.fixture
def tag_credentials():
    return {"name": "tagtest"}


@pytest.fixture
def tag(db, tag_credentials):
    tag = Tag(**tag_credentials)
    tag.save()
