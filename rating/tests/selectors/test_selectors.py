import pytest
from rating.articles.selectors import get_articles, get_rating


@pytest.mark.django_db
def test_get_rating(user1, user2, rating1, rating2, article1, article2):
    a = get_rating(article= article1, user=user1)
    assert a.rating == int(rating1.rating)
    
@pytest.mark.django_db
def test_get_empty_rating(user1, article2):
    a = get_rating(article= article2, user=user1)
    assert a.count() == 0

@pytest.mark.django_db
def test_article_list(user1, user2, rating1, rating2, article1, article2):
    a = get_articles()
    assert len(a) == 2 

