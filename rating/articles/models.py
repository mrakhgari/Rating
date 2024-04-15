from django.db import models
from rating.common.models import BaseModel
from rating.users.models import BaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Article(BaseModel):
    name = models.CharField(max_length=settings.ARTICLE_NAME_LEN, db_index=True, unique=False, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    
    rating_count = models.PositiveBigIntegerField(default=0)
    rating_sum = models.FloatField(default=0)
    
    @property
    def rating_average(self)-> float:
        return 0 if self.rating_count == 0 else self.rating_sum / self.rating_count
    
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
