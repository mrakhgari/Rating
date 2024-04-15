import pytest
from rating.articles.services import create_article


@pytest.mark.django_db
def test_create_article():
    a = create_article(name="pooo", description="CCCContent")

    assert a.name == "pooo"
    assert a.description == "CCCContent"

