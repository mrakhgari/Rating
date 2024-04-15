from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from django.conf import settings

from drf_spectacular.utils import extend_schema


from .models import Article
from .selectors import get_articles
from .services import create_article

class ArticlesAPI(APIView):
    
    class ArticleInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=settings.ARTICLE_NAME_LEN, required=True)
        description = serializers.CharField()
    
    class ArticleOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('name', 'rating_count', 'rating_sum')
    
    
    @extend_schema(responses= ArticleOutputSerializer(many=True) ,tags=["article"])
    def get(self, _):
        articles = get_articles()
        serializer = self.ArticleOutputSerializer(articles, many=True)

        return Response(serializer.data)
    
    @extend_schema(request=ArticleInputSerializer, responses=ArticleOutputSerializer, tags=["article"])
    def post(self, request):
        serializer = self.ArticleInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name, description = serializer.validated_data.get('name'), serializer.validated_data.get('description')

        article = create_article(name=name, description=description)
        serializer = self.ArticleOutputSerializer(article)

        return Response(serializer.data)
        
            
    