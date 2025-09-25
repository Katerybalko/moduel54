from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView,
    create_reply, MyPostRepliesView, accept_reply, decline_reply
)

app_name = 'board'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/reply/', create_reply, name='reply_create'),

    path('my/replies/', MyPostRepliesView.as_view(), name='my_replies'),
    path('replies/<int:pk>/accept/', accept_reply, name='reply_accept'),
    path('replies/<int:pk>/decline/', decline_reply, name='reply_decline'),
]
