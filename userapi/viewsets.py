from rest_framework import viewsets
from . import models
from . import serializers
from datetime import datetime

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = models.Badge.objects.all()
    serializer_class = serializers.BadgeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class GetUserByEmail(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        return models.User.objects.filter(email__exact = email)

class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

# to get user's today's events - as local date is not there, use UTC.
class GetUsersDaysEvents(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        timestamp = int(self.kwargs['timestamp'])
        return models.User.objects.get(userID = userID).events.all().filter(date__startswith =  str(datetime.fromtimestamp(timestamp).date()))

class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.order_by('-timestamp')
    serializer_class = serializers.PostSerializer

class PostLikesViewSet(viewsets.ModelViewSet):
    queryset = models.PostLikes.objects.all()
    serializer_class = serializers.PostLikesSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

class CommentLikesViewSet(viewsets.ModelViewSet):
    queryset = models.CommentLikes.objects.all()
    serializer_class = serializers.CommentLikesSerializer

class FollowingViewSet(viewsets.ModelViewSet):
    queryset = models.Following.objects.all()
    serializer_class = serializers.FollowingSerializer

class IdealDataViewSet(viewsets.ModelViewSet):
    queryset = models.IdealData.objects.all()
    serializer_class = serializers.IdealDataSerializer

class ProductivityViewSet(viewsets.ModelViewSet):
    queryset = models.Productivity.objects.all()
    serializer_class = serializers.ProductivitySerializer

class GetUsersFollowing(viewsets.ModelViewSet):
    serializer_class = serializers.FollowingSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        return models.Following.objects.filter(user_id__exact = userID)

class GetUsersIdealData(viewsets.ModelViewSet):
    serializer_class = serializers.IdealDataSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        return models.IdealData.objects.filter(user_id__exact = userID)

class GetUsersPosts(viewsets.ModelViewSet):
    serializer_class = serializers.UserPostSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        return models.Post.objects.filter(user_id__exact = userID)

class GetPostsLikes(viewsets.ModelViewSet):
    serializer_class = serializers.PostLikesSerializer

    def get_queryset(self):
        postID = self.kwargs['postID']
        return models.PostLikes.objects.filter(post_id__exact = postID)

class GetPostsComments(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        postID = self.kwargs['postID']
        return models.Comment.objects.filter(post_id__exact = postID)

class GetCommentsLikes(viewsets.ModelViewSet):
    serializer_class = serializers.CommentLikesSerializer

    def get_queryset(self):
        commentID = self.kwargs['commentID']
        return models.CommentLikes.objects.filter(comment_id__exact = commentID)

# list(), retrieve(), create(), update(), destroy()