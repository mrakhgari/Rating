import factory

from rating.tests.utils import faker
from rating.users.models import (
        BaseUser,
        )
from rating.articles.models import (
        Article,
        Rating,
        RatingChoices
        )
from django.utils import timezone


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    email    = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    name        = factory.Iterator(['article1', 'article2', 'article3'])
    description    =  factory.Iterator(['des article1', 'des article2', 'des article3'])

class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    article   = factory.SubFactory(ArticleFactory)
    user   = factory.SubFactory(BaseUserFactory)
    rating = factory.LazyAttribute(lambda _: f'{faker.enum(RatingChoices)}')
    created_at           = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    updated_at           = factory.LazyAttribute(lambda _: f'{timezone.now()}')

