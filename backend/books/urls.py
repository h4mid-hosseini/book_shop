from django.urls import path
from . import views


app_name = 'books'


urlpatterns = [
    path('list/',views.BookListAPIView.as_view(), name='books_list'),
    path('reviews/list/',views.get_all_reviews, name='get_reviews'),
    path('reviews/create/',views.create_review, name='create_review'),
    path('reviews/delete/',views.delete_review, name='delete_review'),
    path('reviews/update/',views.update_review, name='update_review'),
    path('suggest/', views.suggest_book_based_on_reviews, name='suggest_books')
]