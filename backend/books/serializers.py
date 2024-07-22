from rest_framework import serializers
from . import models


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Books
        fields = '__all__'



class ReviewsSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    rating = serializers.IntegerField()



class DeleteReviewSerializer(serializers.Serializer):
    review_id = serializers.IntegerField()


class UpdateReviewSerializer(serializers.Serializer):
    review_id = serializers.IntegerField()
    rating = serializers.IntegerField()