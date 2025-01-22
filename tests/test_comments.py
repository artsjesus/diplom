import pytest
from tests.fixtures import create_ad, api_client, create_comment, create_admin_user, create_user


@pytest.mark.django_db
def test_create_comment(api_client, create_user, create_ad):
    """Тест создания комментария"""
    api_client.force_authenticate(user=create_user)
    response = api_client.post(f'/ads/{create_ad.id}/comment_create/', {'text': 'New Comment'})
    assert response.status_code == 201
    assert response.data['text'] == 'New Comment'


@pytest.mark.django_db
def test_list_comments(api_client, create_comment, create_ad):
    """Тест просмотра списка комментариев"""
    response = api_client.get(f'/ads/{create_ad.id}/comment_list/')
    assert response.status_code == 200
    assert len(response.data) > 0


@pytest.mark.django_db
def test_retrieve_comment(api_client, create_ad, create_comment, create_admin_user):
    """Тест просмотра одного комментария"""
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.get(f'/ads/{create_ad.id}/operations/{create_comment.id}/')
    assert response.status_code == 200
    assert response.data['text'] == create_comment.text
    assert str(create_comment) == 'test@example.com - Test Ad'


@pytest.mark.django_db
def test_update_comment(api_client, create_ad, create_admin_user, create_comment):
    """Тест изменения комментария"""
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.patch(f'/ads/{create_ad.id}/operations/{create_comment.id}/', {'text': 'Updated Comment'})
    assert response.status_code == 200
    assert response.data['text'] == 'Updated Comment'


@pytest.mark.django_db
def test_delete_comment(api_client, create_ad, create_admin_user, create_comment):
    """Тест удаления комментария"""
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.delete(f'/ads/{create_ad.id}/operations/{create_comment.id}/')
    assert response.status_code == 204