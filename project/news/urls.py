from django.contrib import admin
from django.urls import path, include
from .views import IndexView, CategoryView, ToggleSubscriptionView

urlpatterns = [
    path('', IndexView.as_view()),
    path('news/', include('news.urls_news')),
    path('articles/', include('news.urls_articles')),
    path('category/<int:pk>', CategoryView.as_view()),
    path('category/<int:pk>/toggle-subscription', ToggleSubscriptionView.as_view(), name='toggle_subscription'),
    #path('hello/', HelloView.as_view())
]