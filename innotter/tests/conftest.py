import pytest
import requests
from page.models import Followers, Page
from page.permissions import (
    IsAdmin,
    IsAdminOrIsModeratorOfThePageOwner,
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
    IsModeratorOfThePageOwner,
    IsPageOwner,
)
from post.models import Post
from post.permissions import IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost
from tag.models import Tag


@pytest.fixture
def is_authenticated_mock(mocker):
    mock = mocker.patch.object(IsAuthenticated, "has_permission")
    return mock


@pytest.fixture
def is_page_owner_mock(mocker):
    mock = mocker.patch.object(IsPageOwner, "has_object_permission")
    return mock


@pytest.fixture
def is_admin_mock(mocker):
    mock = mocker.patch.object(IsAdmin, "has_permission")
    return mock


@pytest.fixture
def is_owner_moderator_mock(mocker):
    mock = mocker.patch.object(IsModeratorOfThePageOwner, "has_object_permission")
    return mock


@pytest.fixture
def is_owner_or_admin_or_moderator_mock(mocker):
    mock = mocker.patch.object(
        IsAdminOrIsOwnerOrIsModeratorOfTheOwner, "has_object_permission"
    )
    return mock


@pytest.fixture
def is_owner_or_admin_or_moderator_post_mock(mocker):
    mock = mocker.patch.object(
        IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost, "has_object_permission"
    )
    return mock


@pytest.fixture
def is_admin_or_owner_moderator_mock(mocker):
    mock = mocker.patch.object(
        IsAdminOrIsModeratorOfThePageOwner, "has_object_permission"
    )
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
    return {"name": "pagetest", "description": "testdesc", "tags": [1]}


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
def post_credentials(page):
    return {"page": page.id, "content": "testcontent"}


@pytest.fixture
def tag(db, tag_credentials):
    tag = Tag.objects.create(**tag_credentials)
    return tag


@pytest.fixture
def post(db, post_credentials):
    page_id = post_credentials["page"]
    del post_credentials["page"]
    post_credentials["page_id"] = page_id
    post = Post.objects.create(**post_credentials)
    return post


@pytest.fixture
def page(db, page_credentials, tag):
    del page_credentials["tags"]
    page = Page.objects.create(**page_credentials)
    page.tags.add(tag.id)
    return page


@pytest.fixture
def follower(page, user_credentials):
    followers = Followers.objects.create(
        page_id=page.id, user=user_credentials.get("uuid")
    )
    return followers
