from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete
from django.urls import path


urlpatterns = [
    #news
    path('', PostList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
]