from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete
from django.urls import path


urlpatterns = [
    path('', PostList.as_view(), name='article_list'),
    path('<int:pk>', PostDetail.as_view(), name='article_detail'),
    path('create/', PostCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]