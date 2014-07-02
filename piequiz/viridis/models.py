import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Test(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, verbose_name='quiz')
    institution = models.CharField(default=None, max_length=200)
    marks = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200)
    pub_date = models.DateTimeField('date', auto_now_add=True)
   
    class Meta:
        verbose_name_plural = 'quizzes'
        verbose_name = 'quiz'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Test, self).save(*args, **kwargs)

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
        return self.pk

class Choice(models.Model):
    choice_text = models.CharField(max_length=500)
    question = models.ForeignKey(Question)
    marks = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
  
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
    user = models.IntegerField()
    test = models.ForeignKey(Test)
    date = models.DateTimeField(auto_now_add=True)
    total_approvals = models.IntegerField(default=0)
