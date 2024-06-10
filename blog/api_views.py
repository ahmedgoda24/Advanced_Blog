from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post, Category, Comment
from .serializers import PostSerializer, CategorySerializer, CommentSerializer,TagSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag
from .filters import PostFilter
# from .paginations import CustomPagination
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    # pagination_class = CustomPagination

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class  = PostSerializer
    queryset = Post.objects.all()

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagListView(generics.ListAPIView):
    serializer_class = TagSerializer  # Adjust this to the appropriate serializer

    def get_queryset(self):
        return Tag.objects.all()

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
