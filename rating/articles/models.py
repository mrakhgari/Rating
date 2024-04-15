from django.db import models
from rating.common.models import BaseModel
from rating.users.models import BaseUser
from django.utils.translation import gettext_lazy as _

class Article(BaseModel):
    name = models.CharField(max_length=100, db_index=True, unique=False, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    
    def __str__(self) -> str:
        return self.name
    
class RatingChoices(models.TextChoices):
    ONE_STAR = 1, _("1 star")
    TWO_STAR = 2, _("2 stars")
    THREE_STAR = 3, _("3 stars")
    FOUR_STAR = 4, _("4 stars")
    FIVE_STAR = 5, _("5 stars")

class Rating(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.PROTECT, related_name='ratings')
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=RatingChoices.choices)
    
    class Meta:
        unique_together = ('article', 'user')  

    def __str__(self) -> str:
        return f"{self.user}'s rating {self.rating}-star for {self.article}"
