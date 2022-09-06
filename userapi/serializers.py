from rest_framework import serializers
from .models import Badge, Comment, CommentLikes, Event, Following, Post, PostLikes, User

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    post_likes = serializers.StringRelatedField(many = True)
    class Meta:
        model = User
        fields = ['userID', 'email', 'firstName', 'lastName', 'isNewUser', 'userName', 'badges', 'lastWeekProductivity', 'post_likes'] # to get only few ('userID', 'firstName', etc)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLikes
        fields = '__all__'

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
# *** https://youtu.be/1k0fRG098cU ***