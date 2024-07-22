from django.urls import path
from . import views


app_name = 'books'


urlpatterns = [
    path('', views.books_filtered_by_genre, name='books_filtered_by_genre'),
    path('list/',views.reviews_list, name='books_list'),
    path('review/list/',views.get_all_reviews, name='get_reviews'),
    path('review/add/',views.create_review, name='create_review'),
    path('review/delete/',views.delete_review, name='delete_review'),
    path('review/update/',views.update_review, name='update_review'),
    path('suggest/', views.suggest_book_based_on_reviews, name='suggest_books')
]