from django.urls import path
from base.views import news_views as views

urlpatterns = [
    path('', views.get_news, name='get_news'),
    path('mynews/', views.get_user_news, name='my_news'),

    path('top/', views.get_top_news, name='get_top_news'),
    path('<str:pk>/', views.get_news_details, name='get_news_details'),
    path('newsitem/create/', views.create_news, name='get_news_details_create_news'),
    path('update/<str:pk>/', views.update_news, name='update_news'),
    path('delete/<str:pk>/', views.delete_news, name='delete_news'),
    path('upload/', views.upload_image, name='upload_news_image'),
    path('<str:pk>/reviews/', views.create_news_review, name='create_news_review'),
    path('<str:pk>/reviews/update/', views.update_news_review, name='update_news_review'),
    path('<str:pk>/reviews/delete/', views.delete_news_review, name='delete_news_review'),
    path('reviews/', views.get_user_reviews, name='get_user_reviews'),

]
