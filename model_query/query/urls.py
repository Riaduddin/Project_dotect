from django.urls import path
from . import views

urlpatterns = [
    path('top-categories/', views.top_categories_view, name='top_categories'),
]
