from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Profile


@receiver(pre_delete, sender=Group)
def delete_users_with_group(sender, instance, **kwargs):
    users_to_delete = User.objects.filter(groups=instance)
    users_to_delete.delete()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()