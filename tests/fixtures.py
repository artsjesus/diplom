import pytest
from rest_framework.test import APIClient
from users.models import User
from ads.models import Ads, Comment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    return User.objects.create(first_name='test', email='test@example.com', password='password123')


@pytest.fixture
def create_admin_user():
    return User.objects.create(first_name='test', role=True, email='admin@example.com', password='adminpass')


@pytest.fixture
def create_ad(create_user):
    return Ads.objects.create(title='Test Ad', price=100, description='Test Description', author=create_user)


@pytest.fixture
def create_comment(create_user, create_ad):
    return Comment.objects.create(text='Test Comment', author=create_user, ad=create_ad)