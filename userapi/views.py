from django.db import IntegrityError
from rest_framework.response import Response

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from userapi.models import Comment, CommentLikes, Event, Following, Post, PostLikes, Productivity, User
from userapi.serializers import CommentLikesSerializer, CommentSerializer, EventSerializer, PostSerializer

import sys
import time
import datetime
from dateutil.tz import *
import json

import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar.events']

# ASSUMES DESCRIPTION IS PRESENT AND ITS FIRST LINE IS type: <type>
def calendar(date = None, event = None):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_new.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # flow = InstalledAppFlow.from_client_secrets_file(
    #             './client_secret_new.json', SCOPES)
    # creds = flow.run_local_server(port=0) # request login and calendar permissions from user

    try:
        service = build('calendar', 'v3', credentials=creds)

        if date is not None: # reading from dB
            start_date = datetime.datetime(date.year, date.month, date.day, 00, 00, 00, 0).isoformat() + 'Z'
            end_date = datetime.datetime(date.year, date.month, date.day, 23, 59, 59, 0).isoformat() + 'Z'

            events_result = service.events().list(calendarId='primary', timeMin=start_date,
                                                timeMax=end_date, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No events found.')
                return None

            calendar_events = [] # list of events read from calendar
            for event in events:
                title = event['summary']
                description = event['description'].split('\n')
                type = description[0].split()[1]
                desc = description[1]
                for i in range(2, len(description)):
                    desc += '\n'
                    desc += description[i]
                start_time = int(datetime.datetime.fromisoformat(event['start']['dateTime']).timestamp())
                end_time = int(datetime.datetime.fromisoformat(event['end']['dateTime']).timestamp())
                date = event['start']['dateTime'][:10]
                calendar_events.append({
                    "type": type,
                    "title": title,
                    "description": desc,
                    "start_time": start_time,
                    "end_time": end_time,
                    "date": date
                })
            print(calendar_events)
            return calendar_events
        
        elif event is not None: # writing to dB
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)
        return None

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getUsersDaysEvents(request, userID, timestamp):
    if request.method == 'GET':
        date = datetime.datetime.fromtimestamp(int(timestamp)).date()
        calendar_events = calendar(date = date)
        
        if calendar_events is not None:
            # add calendar_events to dB
            for event in calendar_events:
                try:
                    # check if event is already added to dB
                    evt = Event.objects.filter(
                        user_id__exact = userID,
                        type__exact = event['type'],
                        title__exact = event['title'],
                        description__exact = event['description'],
                        start_time__exact = event['start_time'],
                        end_time__exact = event['end_time'],
                        date__exact = event['date']
                    )
                    if len(evt) == 0:
                        # create a new event if it is not added to dB
                        Event.objects.create(
                            user_id = userID,
                            type = event['type'],
                            title = event['title'],
                            description = event['description'],
                            start_time = event['start_time'],
                            end_time = event['end_time'],
                            date = event['date']
                        )
                    else:
                        print("Event already added!")
                except:
                    print("Whew!", sys.exc_info()[0], "occurred.")
        
        events = Event.objects.filter(user_id__exact = userID, date__exact = str(date))
        
        send = []
        for event in events:
            serializer = EventSerializer(event)
            send.append(serializer.data)

        return Response({"events": send})

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def addEvent(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        try:
            # check if event is already added to dB
            event = Event.objects.filter(
                    user_id__exact = body_data['userID'],
                    type__exact = body_data['type'],
                    title__exact = body_data['title'],
                    description__exact = body_data['description'],
                    start_time__exact = body_data['start_time'],
                    end_time__exact = body_data['end_time'],
                    date__exact = body_data['date']
                )
            if len(event) == 0:
                # create event if it is not added to dB
                event = Event.objects.create(
                    user_id = body_data['userID'],
                    type = body_data['type'],
                    title = body_data['title'],
                    description = body_data['description'],
                    start_time = body_data['start_time'],
                    end_time = body_data['end_time'],
                    date = body_data['date']
                )
            else:
                event = event[0]
                print("Event already added!")
        except:
            print("Whew!", sys.exc_info()[0], "occurred.")
            return Response({"error": str(sys.exc_info()[0])})
        else:
            # check if the event is already added in calendar
            date = datetime.datetime.strptime(body_data['date'], '%Y-%m-%d').date()
            print(date)
            calendar_events = calendar(date = date)
            exists = False
            if calendar_events is not None:
                for evt in calendar_events:
                    if evt['type'] == body_data['type']:
                        if evt['title'] == body_data['title']:
                            if evt['description'] == body_data['description']:
                                if evt['start_time'] == body_data['start_time']:
                                    if evt['end_time'] == body_data['end_time']:
                                        if evt['date'] == body_data['date']:
                                            exists = True
                                            print("Already added to calendar!")
                                            break
            
            if exists == False:
                # create an event in calendar if not already done
                start_dateTime = datetime.datetime.fromtimestamp(body_data['start_time'])
                from_zone = tzutc()
                to_zone = gettz('Asia/Kolkata')
                start_dateTime.replace(tzinfo=from_zone)
                start_dateTime = start_dateTime.astimezone(to_zone).isoformat()

                end_dateTime = datetime.datetime.fromtimestamp(body_data['end_time'])
                from_zone = tzutc()
                to_zone = gettz('Asia/Kolkata')
                end_dateTime.replace(tzinfo=from_zone)
                end_dateTime = end_dateTime.astimezone(to_zone).isoformat()

                event_data = {
                    'summary': body_data['title'],
                    'description': 'type: ' + body_data['type'] + '\n' + body_data['description'],
                    'start': {
                        'dateTime': start_dateTime,
                        'timeZone': 'Asia/Kolkata',
                    },
                    'end': {
                        'dateTime': end_dateTime,
                        'timeZone': 'Asia/Kolkata',
                    }
                }

                calendar(event = event_data)
            serializer = EventSerializer(event)
            return Response(serializer.data)

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getLastWeekProductivity(request, userID):
    print(userID)
    timestamp = time.time()
    if request.method == "GET":
        scores = []
        for i in range(7):
            date = datetime.datetime.fromtimestamp(timestamp - (7 - i) * 86400).date()
            try:
                scores.append(Productivity.objects.filter(user_id__exact = userID).filter(date__exact = date)[0].score)
            except IndexError:
                scores.append(0)
        return Response({"scores": scores})

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
        Productivity.objects.all().delete()

        user1 = User.objects.create(
            email = "ee18b048@smail.iitm.ac.in",
            firstName = "Pavan Sairam",
            lastName = "D",
            userName = "pavand7",
            
        )
        user1.save()
        lastWeekProductivity = [65.4, 23.7, 89.33, 100, 53.1, 34.8, 79.2]
        timestamp = int(time.time())
        for i in range(7):
            date = datetime.datetime.fromtimestamp(timestamp - (7-i) * 86400).date()
            productivity = Productivity.objects.create(
                user_id = user1.userID,
                date = date,
                score = lastWeekProductivity[i]
            )
            productivity.save()
        user2 = User.objects.create(
            email = "cs20b017@smail.iitm.ac.in",
            firstName = "Biswadip",
            lastName = "Mandal",
            userName = "b.i.s.w_a.d.i.p",
        )
        user2.save()
        lastWeekProductivity = [46.5, 72.3, 93.8, 17.4, 31.5, 83.4, 27.9]
        timestamp = int(time.time())
        for i in range(7):
            date = datetime.datetime.fromtimestamp(timestamp - (7-i) * 86400).date()
            productivity = Productivity.objects.create(
                user_id = user2.userID,
                date = date,
                score = lastWeekProductivity[i]
            )
            productivity.save()
        user3 = User.objects.create(
            email = "cs20b055@smail.iitm.ac.in",
            firstName = "Chetana",
            lastName = "Nayani",
            userName = "nayanichetana003"
        )
        user3.save()
        lastWeekProductivity = [54.6, 27.3, 38.9, 74.1, 15.3, 81.9, 92.7]
        timestamp = int(time.time())
        for i in range(7):
            date = datetime.datetime.fromtimestamp(timestamp - (7-i) * 86400).date()
            productivity = Productivity.objects.create(
                user_id = user3.userID,
                date = date,
                score = lastWeekProductivity[i]
            )
            productivity.save()
        user4 = User.objects.create(
            email = "cs20b008@smail.iitm.ac.in",
            firstName = "Araj",
            lastName = "Khandelwal",
            userName = "araj_khandelwal"
        )
        user4.save()
        lastWeekProductivity = [64.5, 0, 98.3, 32.6, 57.2, 48.3, 88.4]
        timestamp = int(time.time())
        for i in range(7):
            date = datetime.datetime.fromtimestamp(timestamp - (7-i) * 86400).date()
            productivity = Productivity.objects.create(
                user_id = user4.userID,
                date = date,
                score = lastWeekProductivity[i]
            )
            productivity.save()

        event1 = Event.objects.create(
            user_id = user2.userID,
            type = "Exercise",
            title = "Gym",
            description = "Lifted weights for an hour",
            start_time = 1661389200,
            end_time = 1661392800,
            date = "2022-08-25",
        )
        # event1.users.set([user2.userID])
        event1.save()

        event2 = Event.objects.create(
            user_id = user4.userID,
            type = "Study",
            title = "Assignment",
            description = "Solved Math assignment",
            start_time = 1661401800,
            end_time = 1661403600,
            date = "2022-08-25",
        )
        # event2.users.set([user4.userID])
        event2.save()

        event3 = Event.objects.create(
            user_id = user1.userID,
            type = "Entertainment",
            title = "Netflix",
            description = "Watched 2 episodes of F.R.I.E.N.D.S",
            start_time = 1661360400,
            end_time = 1661363100,
            date = "2022-08-24",
        )
        # event3.users.set([user1.userID])
        event3.save()

        event4 = Event.objects.create(
            user_id = user3.userID,
            type = "Study",
            title = "Class",
            description = "Attended Compilers lecture",
            start_time = 1661394600,
            end_time = 1661397600,
            date = "2022-08-25",
        )
        # event4.users.set([user3.userID])
        event4.save()

        event5 = Event.objects.create(
            user_id = user1.userID,
            type = "Exercise",
            title = "Cycling",
            description = "Went for cycling around the campus",
            start_time = 1661346000,
            end_time = 1661349600,
            date = "2022-08-24",
        )
        # event5.users.set([user1.userID,user3.userID])
        event5.save()

        event6 = Event.objects.create(
            user_id = user2.userID,
            type = "Entertainment",
            title = "Movie",
            description = "Watched a movie in theater",
            start_time = 1661344200,
            end_time = 1661355000,
            date = "2022-08-24",
        )
        # event6.users.set([user2.userID,user4.userID])
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