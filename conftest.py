import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rating.users.models import BaseUser
from rating.tests.factories import (
        BaseUserFactory,
        ArticleFactory,
        RatingFactory,
        )


@pytest.fixture
def api_client():
    user = BaseUser.objects.create_user(email='test_user@js.com', password='pass@1test')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def user1_client(user1):
    client = APIClient()
    refresh = RefreshToken.for_user(user1)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client
    

@pytest.fixture
def user1():
    return BaseUserFactory()

@pytest.fixture
def user2():
    return BaseUserFactory()

@pytest.fixture
def article1():
    return ArticleFactory()

@pytest.fixture
def article2():
    return ArticleFactory()


@pytest.fixture
def rating1(article1, user1):
    return RatingFactory(article=article1, user=user1)

@pytest.fixture
def rating2(article1, user2):
    return RatingFactory(article=article1, user=user2)

