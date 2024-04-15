from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rating.api.mixins import ApiAuthMixin

from django.conf import settings

from drf_spectacular.utils import extend_schema


from .models import Article, RatingChoices, Rating
from .selectors import get_articles, get_rating
from .services import create_article, rate_article

class ArticlesAPI(ApiAuthMixin, APIView):
    
    class ArticleInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=settings.ARTICLE_NAME_LEN, required=True)
        description = serializers.CharField()
    
    class ArticleOutputSerializer(serializers.ModelSerializer):
        user_rate = serializers.SerializerMethodField('get_user_rate')
        
        class Meta:
            model = Article
            fields = ('id', 'name', 'rating_count', 'rating_average', 'user_rate')
            
        def get_user_rate(self, article):
            user = self.context.get('request').user
            rating : Rating = get_rating(article=article, user=user)
            if rating:
                return rating.rating
            return None
    
    @extend_schema(responses= ArticleOutputSerializer(many=True) ,tags=["article"])
    def get(self, request):
        articles = get_articles()
        serializer = self.ArticleOutputSerializer(articles, many=True, context={'request':request})

        return Response(serializer.data)
    
    @extend_schema(request=ArticleInputSerializer, responses=ArticleOutputSerializer, tags=["article"])
    def post(self, request):
        serializer = self.ArticleInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name, description = serializer.validated_data.get('name'), serializer.validated_data.get('description')

        article = create_article(name=name, description=description)
        serializer = self.ArticleOutputSerializer(article, context={'request':request})

        return Response(serializer.data)
        
        
class RateAPI(ApiAuthMixin, APIView):
    class RateInputSerializer(serializers.Serializer):
        rate = serializers.ChoiceField(choices=RatingChoices.choices, required=True)

    class RatingOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('name', 'rating_count', 'rating_average', 'ratings')
        
    @extend_schema(request=RateInputSerializer, responses= RatingOutputSerializer, tags=["rate"])
    def post(self, request, id):
        serializer = self.RateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        rate = serializer.validated_data.get('rate')

        article = rate_article(user=user, article_id=id, rate=rate)
        serializer = self.RatingOutputSerializer(article)
        return Response(serializer.data)
            
    