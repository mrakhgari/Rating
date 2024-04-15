from .models import Article, RatingChoices, Rating
from .exceptions import CreateArticleException
from .selectors import get_article, get_rating

from rating.users.models import BaseUser
from django.db import transaction 



def create_article(*, name: str, description: str) -> Article:
    try: 
        article = Article.objects.create(name=name, description=description)
        article.full_clean()
        article.save()
    except:
        raise CreateArticleException()
    return article
    
def rate_first_time(*, article: Article, user: BaseUser, rate: RatingChoices) -> Rating:
    rating = Rating.objects.create(article=article, user=user, rating=rate)
    rating.article.rating_sum += rate
    rating.article.rating_count += 1
    rating.article.full_clean()
    rating.article.save()
    
    rating.full_clean()
    rating.save() 
    return rating
    
def update_rate(*, rating: Rating, rate: RatingChoices) -> Rating:
    previous_rate = rating.rating
    new_value = rate - previous_rate 

    rating.article.rating_sum += new_value
    rating.article.full_clean()
    rating.article.save()
    rating.rating = rate

    rating.full_clean()
    rating.save()
    return rating

@transaction.atomic
def rate_article(*, user: BaseUser, article_id: int, rate: RatingChoices) -> Article:
    article = get_article(id=article_id)
    rating = get_rating(article=article, user=user)
    if not rating: ## first time rating 
        rating = rate_first_time(article=article, user=user, rate=rate)
    else:
        rating = update_rate(rating=rating, rate=rate)

    return rating.article
    
    
    
     