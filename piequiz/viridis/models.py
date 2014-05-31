import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Test(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    institution = models.CharField(default=None, max_length=200)
    marks = models.IntegerField(default=0)
    slug = models.SlugField()
    pub_date = models.DateTimeField('date-published')

    def __unicode__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
