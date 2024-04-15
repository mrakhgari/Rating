from django.urls import path
from .apis import ArticlesAPI


urlpatterns = [
    path('', ArticlesAPI.as_view(),name="articles"),
]
