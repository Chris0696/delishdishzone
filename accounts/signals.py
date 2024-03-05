from .models import *
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('User profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('User is updated')
        except:
            # Create UserProfile if not existe
            UserProfile.objects.create(user=instance)
            print('Profile was not existe but I create one')
        print('User profile is updated')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    print(instance.username, 'this user is being saved')

# post_save.connect(create_user_profile, sender=User)