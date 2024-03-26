from django.db import models
from accounts.models import User, UserProfile
from .utils import send_notification


# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=128, null=False, unique=True)
    restaurant_address = models.CharField(max_length=150)
    restaurant_phone = models.CharField(max_length=150)
    restaurant_license = models.ImageField(upload_to='vendors/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'vendor/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved:
                    # Send notification mail
                    mail_subject = 'Congratulation! Your restaurant has been approved'
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification mail
                    mail_subject = "We're sorry! You're not eligible for publish your food menu on DDZone marketplace"
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)



















