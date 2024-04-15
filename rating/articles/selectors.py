from django.db.models import QuerySet
from .models import Article

def get_articles() -> QuerySet[Article]:
    return Article.objects.all()
