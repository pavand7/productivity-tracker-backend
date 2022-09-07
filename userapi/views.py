from django.db import IntegrityError
from rest_framework.response import Response

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from userapi.models import Comment, CommentLikes, Event, Following, Post, PostLikes, User
from userapi.serializers import CommentLikesSerializer, CommentSerializer, PostSerializer

import time
import json
# Create your views here.

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def addComment(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        try:
            Comment.objects.create(
                post_id = body_data['postID'],
                user_id = body_data['userID'],
                body = body_data['body'],
                timestamp = int(time.time())
            )
        except IntegrityError:
            print()
        else:
            post = Post.objects.get(postID = body_data['postID'])
            post.numComments += 1
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def deleteComment(request):
    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        try:
            comment = Comment.objects.get(commentID = body_data['commentID'])
            postID = comment.post_id
            comment.delete()
        except IntegrityError:
            print()
        else:
            post = Post.objects.get(postID = postID)
            post.numComments -= 1
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def likePost(request, postID, userID):
    if request.method == 'POST':
        # postID = request.data.get('postID')
        # userID = request.data.get('userID')
        try:
            PostLikes.objects.create(post_id = postID, user_id = userID)
        except IntegrityError:
            print()
        else:
            post = Post.objects.get(postID = postID)
            post.numLikes += 1
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def unLikePost(request, postID, userID):
    if request.method == 'POST':
        # postID = request.data.get('postID')
        # userID = request.data.get('userID')
        try:
            PostLikes.objects.filter(post_id = postID, user_id = userID).delete()
        except IntegrityError:
            print()
        else:
            post = Post.objects.get(postID = postID)
            post.numLikes -= 1
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def likeComment(request, commentID, userID):
    if request.method == 'POST':
        # commentID = request.data.get('commentID')
        # userID = request.data.get('userID')
        try:
            CommentLikes.objects.create(comment_id = commentID, user_id = userID)
        except IntegrityError:
            print()
        else:
            comment = Comment.objects.get(commentID = commentID)
            comment.numLikes += 1
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def unLikeComment(request, commentID, userID):
    if request.method == 'POST':
        # commentID = request.data.get('commentID')
        # userID = request.data.get('userID')
        try:
            CommentLikes.objects.filter(comment_id = commentID, user_id = userID).delete()
        except IntegrityError:
            print()
        else:
            comment = Comment.objects.get(commentID = commentID)
            comment.numLikes -= 1
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def createTables(request):
    if request.method == "GET":
        User.objects.all().delete()
        Event.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        PostLikes.objects.all().delete()
        CommentLikes.objects.all().delete()
        Following.objects.all().delete()

        user1 = User.objects.create(
            email = "ee18b048@smail.iitm.ac.in",
            firstName = "Pavan Sairam",
            lastName = "D",
            userName = "pavand7",
            lastWeekProductivity = [65.4, 23.7, 89.33, 100, 53.1, 34.8, 79.2]
        )
        user1.save()
        user2 = User.objects.create(
            email = "cs20b017@smail.iitm.ac.in",
            firstName = "Biswadip",
            lastName = "Mandal",
            userName = "b.i.s.w_a.d.i.p",
            lastWeekProductivity = [46.5, 72.3, 93.8, 17.4, 31.5, 83.4, 27.9]
        )
        user2.save()
        user3 = User.objects.create(
            email = "cs20b055@smail.iitm.ac.in",
            firstName = "Chetana",
            lastName = "Nayani",
            userName = "nayanichetana003",
            lastWeekProductivity = [54.6, 27.3, 38.9, 74.1, 15.3, 81.9, 92.7]
        )
        user3.save()
        user4 = User.objects.create(
            email = "cs20b008@smail.iitm.ac.in",
            firstName = "Araj",
            lastName = "Khandelwal",
            userName = "araj_khandelwal",
            lastWeekProductivity = [64.5, 0, 98.3, 32.6, 57.2, 48.3, 88.4]
        )
        user4.save()

        event1 = Event.objects.create(
            type = "Exercise",
            title = "Gym",
            description = "Lifted weights for an hour",
            start_time = 1661389200,
            end_time = 1661392800,
            date = "2022-08-25",
        )
        event1.users.set([user2.userID])
        event1.save()

        event2 = Event.objects.create(
            type = "Study",
            title = "Assignment",
            description = "Solved Math assignment",
            start_time = 1661401800,
            end_time = 1661403600,
            date = "2022-08-25",
        )
        event2.users.set([user4.userID])
        event2.save()

        event3 = Event.objects.create(
            type = "Entertainment",
            title = "Netflix",
            description = "Watched 2 episodes of F.R.I.E.N.D.S",
            start_time = 1661360400,
            end_time = 1661363100,
            date = "2022-08-24",
        )
        event3.users.set([user1.userID])
        event3.save()

        event4 = Event.objects.create(
            type = "Study",
            title = "Class",
            description = "Attended Compilers lecture",
            start_time = 1661394600,
            end_time = 1661397600,
            date = "2022-08-25",
        )
        event4.users.set([user3.userID])
        event4.save()

        event5 = Event.objects.create(
            type = "Exercise",
            title = "Cycling",
            description = "Went for cycling around the campus",
            start_time = 1661346000,
            end_time = 1661349600,
            date = "2022-08-24",
        )
        event5.users.set([user1.userID,user3.userID])
        event5.save()

        event6 = Event.objects.create(
            type = "Entertainment",
            title = "Movie",
            description = "Watched a movie in theater",
            start_time = 1661344200,
            end_time = 1661355000,
            date = "2022-08-24",
        )
        event6.users.set([user2.userID,user4.userID])
        event6.save()

        post1 = Post.objects.create(
            user_id = user3.userID,
            body = "Found this very interesting article about Google, do check it out.",
            timestamp = int(time.time())
        )
        post1.save()

        post2 = Post.objects.create(
            user_id = user2.userID,
            body = "Phew!! Finally some rain amidst this scorching heat!",
            timestamp = int(time.time())
        )
        post2.save()

        post3 = Post.objects.create(
            user_id = user4.userID,
            body = "Liking this app so much :)",
            timestamp = int(time.time())
        )
        post3.save()

        post4 = Post.objects.create(
            user_id = user1.userID,
            body = "Hey there! We can also post in this space.",
            timestamp = int(time.time())
        )
        post4.save()

        post = Post.objects.get(user_id = user1.userID)
        comment1 = Comment.objects.create(
            post_id = post.postID,
            user_id = user3.userID,
            body = "We can also comment. Haha!",
            timestamp = int(time.time())
        )
        comment1.save()
        post.numComments += 1
        post.save()

        comment2 = Comment.objects.create(
            post_id = post.postID,
            user_id = user2.userID,
            body = "Like, unlike works tooooo.",
            timestamp = int(time.time())
        )
        comment2.save()
        post.numComments += 1
        post.save()

        post = Post.objects.get(user_id = user2.userID)
        comment3 = Comment.objects.create(
            post_id = post.postID,
            user_id = user4.userID,
            body = "Heaven onlyyyy",
            timestamp = int(time.time())
        )
        comment3.save()
        post.numComments += 1
        post.save()

        post = Post.objects.get(user_id = user3.userID)
        comment4 = Comment.objects.create(
            post_id = post.postID,
            user_id = user4.userID,
            body = "Insightful.",
            timestamp = int(time.time())
        )
        comment4.save()
        post.numComments += 1
        post.save()

        post = Post.objects.get(user_id = user4.userID)
        postLikes1 = PostLikes.objects.create(
            post_id = post.postID,
            user_id = user1.userID
        )
        postLikes1.save()
        post.numLikes += 1
        post.save()

        postLikes2 = PostLikes.objects.create(
            post_id = post.postID,
            user_id = user2.userID
        )
        postLikes2.save()
        post.numLikes += 1
        post.save()

        postLikes3 = PostLikes.objects.create(
            post_id = post.postID,
            user_id = user3.userID
        )
        postLikes3.save()
        post.numLikes += 1
        post.save()

        post = Post.objects.get(user_id = user2.userID)
        postLikes4 = PostLikes.objects.create(
            post_id = post.postID,
            user_id = user4.userID
        )
        postLikes4.save()
        post.numLikes += 1
        post.save()

        post = Post.objects.get(user_id = user3.userID)
        postLikes5 = PostLikes.objects.create(
            post_id = post.postID,
            user_id = user1.userID
        )
        postLikes5.save()
        post.numLikes += 1
        post.save()

        comment = Comment.objects.get(body = "Like, unlike works tooooo.")
        commentLikes1 = CommentLikes.objects.create(
            comment_id = comment.commentID,
            user_id = user1.userID
        )
        commentLikes1.save()
        comment.numLikes += 1
        comment.save()

        comment = Comment.objects.get(body = "Heaven onlyyyy")
        commentLikes2 = CommentLikes.objects.create(
            comment_id = comment.commentID,
            user_id = user2.userID
        )
        commentLikes2.save()
        comment.numLikes += 1
        comment.save()

        serializer = CommentLikesSerializer(commentLikes2)
        return Response(serializer.data)
    return []