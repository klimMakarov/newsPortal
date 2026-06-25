from django.contrib import admin
from django.urls import path, include
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('news/', include('news.urls_news')),
    path('articles/', include('news.urls_articles')),
]