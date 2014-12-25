import datetime
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class TestVoteCountManager(models.Manager):
    def get_queryset(self):
        return super(TestVoteCountManager,
self).get_queryset().annotate(
        votes=Count('vote')).order_by('-rank_score', '-votes')

class Test(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, verbose_name='quiz')
    institution = models.CharField(default=None, max_length=200)
    marks = models.IntegerField(default=0)
    marks_per_question = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200)
    rank_score = models.FloatField(default=0.0)
    pub_date = models.DateTimeField('date', auto_now_add=True)
    with_votes = TestVoteCountManager()
    objects = models.Manager()

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

    def set_rank(self):
        # Based on HN ranking algo
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2

        delta = now() - self.submitted_on
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Question(models.Model):
    question_text = models.CharField(max_length = 1000)
    question_pic = models.ImageField(upload_to='images/', blank=True)
    test = models.ForeignKey(Test)
    marks = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length=500)
    question = models.ForeignKey(Question)
    test_id = models.IntegerField()
    is_correct = models.NullBooleanField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.id)

class Vote(models.Model):
    voter = models.ForeignKey(User)
    test = models.ForeignKey(Test)

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.test.title)

class History(models.Model):
    user = models.ForeignKey(User)
    test = models.CharField(max_length=200)
    test_id = models.IntegerField()
    score = models.IntegerField()
    marks = models.IntegerField()
    pub_date = models.DateTimeField(auto_now=True)
