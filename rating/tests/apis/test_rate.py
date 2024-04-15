import pytest
from django.urls import reverse
import json


@pytest.mark.django_db
def test_list_articles_api(user1_client, rating1):
    url_ = reverse("api:articles:articles")
    
    response = user1_client.get(url_, content_type="application/json")
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data[0].get('user_rate') == int(rating1.rating)


