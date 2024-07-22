from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status, response, views
from . import models, serializers




class BookListAPIView(views.APIView):
    serializer_class = serializers.BooksSerializer
    
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books_books")
            rows = cursor.fetchall()

        reviews = [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in rows]

        return response.Response(reviews, status=status.HTTP_200_OK)
    



@api_view(['GET'])
def get_all_reviews(request):
    """
    this method returns all reviews that user made yet
    """

    user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books_reviews WHERE user_id = %s", [user_id])
        rows = cursor.fetchall()

    reviews = [{'id': row[0], 'book': row[1], 'user': row[2], 'rating': row[3]} for row in rows]

    return response.Response(reviews, status=status.HTTP_200_OK)




@api_view(['POST'])
def create_review(request):
    """
    with user can add new review to books 
    hevncre is what we expect to be sent for creating new review:
    - book_id:type(int)
    - rating:type(int)

    duplicated review is not allowed as we defined in models
    """

    serializer = serializers.ReviewSerializer(data=request.data)

    if serializer.is_valid():
        book_id = serializer.validated_data['book_id']
        rating = serializer.validated_data['rating']
        user_id = request.user.id

        query = """
        INSERT INTO reviews (book_id, user_id, rating)
        VALUES (%s, %s, %s);
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [book_id, user_id, rating])
            return response.Response({'status': 'Review created'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PATCH'])
def update_review(request):
    """
    here user can update review.
    user should send these:
    - review_id : type(int)
    - rating: type(int)
    """

    serializer = serializers.UpdateReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        review_id = serializer.validated_data['review_id']
        rating = serializer.validated_data['rating']
        user_id = request.user.id
        
        query = """
        UPDATE reviews
        SET rating = %s
        WHERE id = %s AND user_id = %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [rating, review_id, user_id])
        
        
        if cursor.rowcount == 0:
            return response.Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return response.Response({'status': 'Review updated'}, status=status.HTTP_200_OK)
    else:
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
def delete_review(request):
    """
    this method can delete user reviews.
    user should only send the review ID to delete it.
    if the review does not belong to user or did not found, 404 will be returned.
    """
    
    serializer = serializers.DeleteReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        review_id = serializer.validated_data['review_id']
        user_id = request.user.id

        query = """
        DELETE FROM reviews
        WHERE id = %s AND user_id = %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [review_id, user_id])
        
        if cursor.rowcount == 0:
            return response.Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return response.Response({'status': 'Review deleted'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def suggest_book_based_on_reviews(request):
    pass