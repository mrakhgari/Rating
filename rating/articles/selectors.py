from django.db.models import QuerySet
from .exceptions import ArticleNotFoundException
from .models import Article, Rating
from rating.users.models import BaseUser

def get_articles() -> QuerySet[Article]:
    return Article.objects.all()

def get_article(*, id: int) -> Article:
    article = Article.objects.filter(id=id)
    
    if not article.exists():
        raise ArticleNotFoundException()
    
    return article.first()

def get_rating(*, article: Article, user: BaseUser):
    rating = Rating.objects.select_for_update().filter(article=article, user=user)
    if rating.exists():
        return rating.first()

    return rating.none()