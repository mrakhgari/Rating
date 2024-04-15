from .models import Article
from .exceptions import CreateArticleException

def create_article(*, name: str, description: str) -> Article:
    try: 
        article = Article.objects.create(name=name, description=description)
        article.full_clean()
        article.save()
    except:
        raise CreateArticleException()
    return article
    