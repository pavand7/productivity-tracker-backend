from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

# Create your models here.

# *** Check each of the field and try to use options effectively ***

def last_week_productivity_default():
    return [-1.0] * 7

class Badge(models.Model):
    badgeID = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 20)
    description = models.TextField()
    #photo = models.ImageField()

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique = True)
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    isNewUser = models.BooleanField(default = True)
    userName = models.CharField(unique = True, max_length = 20)
    # photo = models.ImageField(upload_to = )
    badges = models.ManyToManyField(Badge, related_name = 'users', blank = True) # many-to-many: a user can have multiple badges and a badge can be awarded to multiple users
    lastWeekProductivity = ArrayField(size = 7, base_field = models.FloatField(), default = last_week_productivity_default)

class Event(models.Model):
    eventID = models.AutoField(primary_key=True)
    users = models.ManyToManyField(User, related_name = 'events') # many-to-many: an event can be done by multiple users and a user can have multiple events
    type = models.CharField(max_length = 50)
    title = models.CharField(max_length = 20)
    description = models.TextField()
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField()
    date = models.CharField(max_length = 10)

class Post(models.Model):
    postID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name = 'posts', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.BigIntegerField()
    numLikes = models.BigIntegerField(default = 0)
    numComments = models.BigIntegerField(default = 0)

class PostLikes(models.Model):
    post = models.ForeignKey(Post, related_name = 'likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'post_likes', on_delete=models.CASCADE)

    def __str__(self):
        return '%d' % (self.id)

    class Meta:
        unique_together = ['post', 'user']

class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name = 'comments', on_delete=models.CASCADE) # many-to-one: a post can have multiple comments
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.BigIntegerField()
    numLikes = models.BigIntegerField(default = 0)

class CommentLikes(models.Model):
    comment = models.ForeignKey(Comment, related_name = 'likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'comment_likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['comment', 'user']

class Following(models.Model):
    user = models.ForeignKey(User, related_name = 'following', on_delete=models.CASCADE)
    following = models.BigIntegerField()