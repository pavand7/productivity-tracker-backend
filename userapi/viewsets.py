from rest_framework import viewsets, mixins
from . import models
from . import serializers

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = models.Badge.objects.all()
    serializer_class = serializers.BadgeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class GetUserByEmail(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        return models.User.objects.filter(email__exact = email)

class EventViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

class GetPostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Post.objects.order_by('-timestamp')
    serializer_class = serializers.GetPostSerializer

class PostViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = models.Post.objects.order_by('-timestamp')
    serializer_class = serializers.PostSerializer

class PostLikesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.PostLikes.objects.all()
    serializer_class = serializers.PostLikesSerializer

class CommentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

class CommentLikesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.CommentLikes.objects.all()
    serializer_class = serializers.CommentLikesSerializer

class FollowingViewSet(viewsets.ModelViewSet):
    queryset = models.Following.objects.all()
    serializer_class = serializers.FollowingSerializer

class IdealDataViewSet(viewsets.ModelViewSet):
    queryset = models.IdealData.objects.all()
    serializer_class = serializers.IdealDataSerializer

class ProductivityViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Productivity.objects.all()
    serializer_class = serializers.ProductivitySerializer

class GetUsersFollowing(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.FollowingSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        return models.Following.objects.filter(user_id__exact = userID)

class GetUsersIdealData(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.IdealDataSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        return models.IdealData.objects.filter(userID__exact = userID)

class GetUsersPosts(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserPostSerializer

    def get_queryset(self):
        userID = self.kwargs['userID']
        return models.Post.objects.filter(user_id__exact = userID)

class GetPostsLikes(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.PostLikesSerializer

    def get_queryset(self):
        postID = self.kwargs['postID']
        return models.PostLikes.objects.filter(post_id__exact = postID)

class GetPostsComments(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        postID = self.kwargs['postID']
        return models.Comment.objects.filter(post_id__exact = postID)

class GetCommentsLikes(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CommentLikesSerializer

    def get_queryset(self):
        commentID = self.kwargs['commentID']
        return models.CommentLikes.objects.filter(comment_id__exact = commentID)

# list(), retrieve(), create(), update(), destroy()