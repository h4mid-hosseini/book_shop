from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)


    class Meta:
        unique_together = ('title', 'author', 'genre')
    



class Reviews(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'user'], name='unique_user_book_review'),
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='rating_range')
        ]

    def __str__(self):
        return f'Review of {self.book.title} by {self.user.username}'

