from django.urls import path
from .apis import ArticlesAPI, RateAPI


urlpatterns = [
    path('', ArticlesAPI.as_view(),name="articles"),
    path('<int:id>/rate/', RateAPI.as_view(), name='rating')
]
