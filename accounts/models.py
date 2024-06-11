from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15,null=True , blank=True)
    addres = models.CharField(max_length=50 , blank=True, null=True)
    bio = models.CharField(max_length=50 , blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/'  , blank=True, null=True)
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("accounts:profile/profile_edit", kwargs={"pk": self.pk})

# @receiver(post_save , sender=User)
# def create_user_profile(sender,instance,created , **kwargs):
#     if created:
#         Profile.objects.create(
#             user = instance
#         )
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)