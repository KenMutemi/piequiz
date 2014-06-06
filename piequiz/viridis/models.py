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

    def get_absolute_url(self):
        return "/%s/%s" % (self.id, self.slug)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Question(models.Model):
    question_text = models.CharField(max_length = 1000)
    test = models.ForeignKey(Test)
    marks = models.IntegerField(default=0)
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length = 500)
    question = models.ForeignKey(Question)
    marks = models.IntegerField(default=0)
    pub_date = models.DateTimeField()
  
    def __unicode__(self):
        return self.choice_text

class Answer(models.Model):
    user = models.IntegerField()
    choice = models.ForeignKey(Choice)
    test = models.IntegerField()
    answer_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.choice

class Approve(models.Model):
    user = models.ManyToManyField(User, related_name='approves')
    test = models.ForeignKey(Test)
    date = models.DateTimeField(auto_now_add=True)
    total_approvals = models.IntegerField(default=0)
