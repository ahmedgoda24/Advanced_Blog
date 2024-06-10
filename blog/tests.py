from django.test import TestCase

# Create your tests here.


# blog_app/tests/test_models.py
from django.test import TestCase , Client
from django.contrib.auth.models import User
from blog.models import Post, Category, Comment
from django.utils.text import slugify
from django.urls import reverse
from taggit.models import Tag

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

class BlogAppViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Django')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,  # Pass the User instance here
            content='This is a test comment.'
        )
        # Adding tags to the post for testing
        self.post.tags.add('testing', 'django')

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_search_view(self):
        response = self.client.get(reverse('post_list'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_posts_by_category_view(self):
        response = self.client.get(reverse('posts_by_category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_posts_by_tags_view(self):
        tag = Tag.objects.get(name='testing')
        response = self.client.get(reverse('posts_by_tags', kwargs={'slug': tag.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_create.html')

        response = self.client.post(reverse('post_create'), {
            'title': 'New Post',
            'content': 'This is a new post.',
            'author': self.user.id,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post creation

    def test_post_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')

        response = self.client.post(reverse('post_update', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Post',
            'content': 'This is an updated post.',
            'author': self.user.id,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post update

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

        response = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful post deletion

    def test_add_comment_to_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_comment_to_post', kwargs={'pk': self.post.pk}), {
            'content': 'Another test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful comment addition
        self.assertEqual(Comment.objects.count(), 2)

    # Additional test to ensure only authenticated users can create, update, and delete posts
    def test_post_create_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post_create'))
        self.assertRedirects(response, '/accounts/login/?next=/blog/create/')

    def test_post_update_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post_update', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/blog/{self.post.pk}/edit/')

    def test_post_delete_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/blog/{self.post.pk}/delete/')