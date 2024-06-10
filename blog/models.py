from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify


class Post(models.Model):
    author = models.ForeignKey(User,related_name='post_author' , on_delete=models.CASCADE ,)
    title = models.CharField(max_length=50 )
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at=models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('Category', related_name='post_category', on_delete=models.CASCADE )
    tags = TaggableManager(blank=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.title)    
       super(Post, self).save(*args, **kwargs) # Call the real save() method


       

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})



class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(blank=True, null=True)


    def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.name)    
       super(Category, self).save(*args, **kwargs) # Call the real save() method

        

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User,related_name='comment_author' , on_delete=models.CASCADE ,)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)


    def __str__(self):
        return self.content