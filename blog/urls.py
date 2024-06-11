from django.urls import path,include
from . import views
from . import api_views
from .api_views import PostListCreateView, PostDetailView, CategoryListView, TagListView, CommentListCreateView, CommentDetailView
from rest_framework import routers
from rest_framework.routers import DefaultRouter



app_name = 'blog'


urlpatterns = [
   

    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('/post', views.PostCreateView.as_view(), name='post'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/comment/', views.AddCommentToPostView.as_view(), name='add_comment_to_post'),
    # ----------------------------------------------------------------------------
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create-api'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post--api'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/tags/', TagListView.as_view(), name='tag-list'),
    path('api/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('api/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),



    
 
]

