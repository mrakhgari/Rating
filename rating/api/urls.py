from django.urls import path, include

urlpatterns = [
    path('users/', include(('rating.users.urls', 'users'))),
    path('articles/', include(('rating.articles.urls', 'articles'))),
]
