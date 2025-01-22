import pytest
from tests.fixtures import create_ad, create_user, api_client


@pytest.mark.django_db
def test_retrieve_ad(api_client, create_user, create_ad):
    """Тест просмотра одного объявления"""
    api_client.force_authenticate(user=create_user)
    response = api_client.get(f'/ads/detail/{create_ad.pk}/')
    assert response.status_code == 200
    assert response.data['title'] == create_ad.title
    assert str(create_ad) == 'Test Ad'


@pytest.mark.django_db
def test_update_ad(api_client, create_user, create_ad):
    """Тест изменения объявления"""
    api_client.force_authenticate(user=create_user)
    response = api_client.patch(f'/ads/update/{create_ad.pk}/', {'title': 'Updated Title'})
    assert response.status_code == 200
    assert response.data['title'] == 'Updated Title'


@pytest.mark.django_db
def test_create_ad(api_client, create_user):
    """Тест создания одного объявления"""
    api_client.force_authenticate(user=create_user)
    response = api_client.post('/ads/create/', {'title': 'New Ad', 'price': 200, 'description': 'Ad description'})
    assert response.status_code == 201
    assert response.data['title'] == 'New Ad'


@pytest.mark.django_db
def test_list_ads(api_client, create_ad):
    """Тест просмотра списка объявления"""
    response = api_client.get('/ads/list/')
    assert response.status_code == 200
    assert len(response.data['results']) > 0


@pytest.mark.django_db
def test_delete_ad(api_client, create_user, create_ad):
    """Тест удаления объявления"""
    api_client.force_authenticate(user=create_user)
    response = api_client.delete(f'/ads/delete/{create_ad.id}/')
    assert response.status_code == 204