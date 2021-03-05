from django.db import models

# Create your models here.
from django.conf import settings

from django.utils.text import slugify

class Question1(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField()
    group = models.ForeignKey('QuestionGroups', on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    objects = models.Manager()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question1, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title


class Answers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question1, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    objects = models.Manager()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_likes")
    def count_likes(self):
        return self.likes.count()
    def check_like(self,user23):
        return self.likes.filter(id=user23.id).exists()
    def __unicode__(self):
        return self.id


class QuestionGroups(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()
    def __unicode__(self):
        return self.name
