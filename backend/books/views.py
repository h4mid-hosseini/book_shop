from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status, response, views
from . import models, serializers







@api_view(['GET'])
def reviews_list(request):
    '''
        this class is just used to check list of review to see changes made by different methods I'm using
    '''
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books_books")
        rows = cursor.fetchall()

    reviews = [
        {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'genre': row[3]
        } 
        for row in rows
        ]

    return response.Response(reviews, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_all_reviews(request):
    """
        this method returns all reviews that user made yet
    """

    user_id = request.user.id
    print('user id: ', user_id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books_reviews WHERE user_id = %s", [user_id])
        rows = cursor.fetchall()

    reviews = [
        {
            'id': row[0],
            'rating': row[1],
            'book': row[2],
            'user': row[3]
        } 
        for row in rows
        ]

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

    serializer = serializers.ReviewsSerializer(data=request.data)

    if serializer.is_valid():
        book_id = serializer.validated_data['book_id']
        rating = serializer.validated_data['rating']
        user_id = request.user.id

        query = """
        INSERT INTO books_reviews (book_id, user_id, rating)
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
        UPDATE books_reviews
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
        DELETE FROM books_reviews
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
def books_filtered_by_genre(request):
    """
        this function return books based on the genre user specified
        user should put genre in url like below:
        - /api/books/Advanture
        above url return books in Advanture genre
    """

    genre = request.GET.get('genre', None)

    if genre != None:
        query = """
        SELECT * FROM books_books
        WHERE genre = %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [genre])
            rows = cursor.fetchall()

        reviews = [
            {
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'genre': row[3]
            } 
            for row in rows
            ]

        return response.Response(reviews, status=status.HTTP_200_OK)
    
    return response.Response(status=status.HTTP_400_BAD_REQUEST)




# @api_view(['GET'])
# def suggest_book_based_on_reviews(request):

#     review = models.Reviews.objects.filter(user=request.user).order_by('-rating')
#     if review != []:
#         most_loved_genre = review[0]
#         genre = most_loved_genre.book.genre
#         books = models.Books.objects.filter(genre=genre)
#         data = serializers.BooksSerializer(books, many=True)

#         return response.Response(data.data, status=status.HTTP_200_OK)
    

#     return response.Response({'info':'there is not enough data about you'}, status=status.HTTP_204_NO_CONTENT)





@api_view(['GET'])
def suggest_book_based_on_reviews(request):
    '''
        this view retuns list of books user may like based on review history
    '''
    user_id = request.user.id
    
    review_query = """
    SELECT book_id
    FROM books_reviews
    WHERE user_id = %s
    ORDER BY rating DESC
    LIMIT 1;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(review_query, [user_id])
        row = cursor.fetchone()
        print(row)
    
    if row:
        book_id = row[0]
        
        genre_query = """
        SELECT genre
        FROM books_books
        WHERE id = %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(genre_query, [book_id])
            row = cursor.fetchone()
        
        if row:
            genre = row[0]
            
            books_query = """
            SELECT * 
            FROM books_books
            WHERE genre = %s;
            """
            
            with connection.cursor() as cursor:
                cursor.execute(books_query, [genre])
                books = cursor.fetchall()
            
            if books:

                books_data = [
                    {
                        'id': book[0],
                        'title': book[1],
                        'author': book[2],
                        'genre': book[3],
                    }
                    for book in books
                ]
                
                return response.Response(books_data, status=status.HTTP_200_OK)
    
    return response.Response({'info': 'There is not enough data about you'}, status=status.HTTP_204_NO_CONTENT)
