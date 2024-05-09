from django.db import models
from accounts.models import User, UserProfile
from .utils import send_notification
from datetime import time, date, datetime


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

    def is_open(self):
        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()

        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print(current_time)

        is_open = None

        for hour in current_opening_hours:
            if not hour.is_closed:
                start = str(datetime.strptime(hour.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(hour.to_hour, "%I:%M %p").time())
                if start < current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'vendor/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
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


DAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),

]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in
                  (0, 30)]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['day', '-from_hour']
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return f'{self.get_day_display()}'
