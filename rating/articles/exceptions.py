from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class CreateArticleException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred. We could not create the article.')
    
    
class ArticleNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('We could not find an article with this id.')
    
    
    
    
    