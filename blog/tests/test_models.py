
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Category, Comment
from django.utils.text import slugify

class BlogAppModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Django')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )
    
    def comment_create(self):
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user.username,
            content='This is a test comment.'
        )

    def test_post_creation(self):
        post = self.post
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.title)
        self.assertEqual(post.slug, slugify(post.title))

    def test_category_creation(self):
        category = self.category
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), category.name)
        self.assertEqual(category.slug, slugify(category.name))

