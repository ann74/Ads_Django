import pytest


@pytest.mark.django_db
def test_ads_create(client, user_token, categories):
    response = client.post(
        "/ad/",
        {
            "name": "new test ad",
            "price": 500,
            "is_published": False,
            "category": categories.name
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}")

    assert response.status_code == 201
    assert response.data == {
        'id': 12,
        'author': 'username',
        'category': categories.name,
        'description': '',
        'image': None,
        'is_published': False,
        'name': 'new test ad',
        'price': 500,
    }
