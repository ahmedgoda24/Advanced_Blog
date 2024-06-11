


    

from django.test import TestCase , Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category
from blog.forms import CommentForm


class BlogAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Django', slug='django')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog:post'), {
            'title': 'New Post',
            'content': 'New Content',
            'author': self.user.id,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 200)

    def test_post_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog:post_update', args=[self.post.pk]), {
            'title': 'Updated Post',
            'content': 'Updated Content',
            'author': self.user.id,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog:post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)






class AddCommentToPostViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a category
        self.category = Category.objects.create(name='Test Category')
        
        # Create a post
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user,
            category=self.category
        )
        
        # URL for adding comment
        self.url = reverse('blog:add_comment_to_post', args=[self.post.pk])

    def test_add_comment_to_post_get(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')
        
        # GET request to add comment view
        response = self.client.get(self.url)
        
        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'blog/add_comment_to_post.html')
        
        # Check if the form is in the context
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_add_comment_to_post_post(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')
        
        # POST request to add comment view
        response = self.client.post(self.url, {
            'content': 'This is a test comment.'
        })
        
        # Check if the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        
        # Check if the comment is associated with the post
        comment = Comment.objects.first()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)
        
        # Check if the response is a redirect to the post detail view
        self.assertRedirects(response, self.post.get_absolute_url())

    def test_add_comment_to_post_not_logged_in(self):
        # POST request to add comment view without logging in
        response = self.client.post(self.url, {
            'content': 'This is a test comment.'
        })
        
        # Check if the response is a redirect to the login page
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
        
        # Check if no comment was created
        self.assertEqual(Comment.objects.count(), 0)