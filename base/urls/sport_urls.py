from django.urls import path
from base.views import sport_views as views

urlpatterns = [
    path('', views.get_sport, name="sport"),
    path('top/', views.get_top_sport, name="top-sport"),
    path('create/', views.create_sport, name="create-sport"),
    path('<str:pk>/', views.get_sport_details, name="sport-details"),
    path('<str:pk>/reviews/', views.create_sport_review, name="create-sport-review"),
    path('<str:pk>/update/', views.update_sport, name="update-sport"),
    path('<str:pk>/delete/', views.delete_sport, name="delete-sport"),
    path('image/upload/', views.upload_image, name="upload-image"),
]
