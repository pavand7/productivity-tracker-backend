from userapi.viewsets import BadgeViewSet, CommentLikesViewSet, CommentViewSet, EventViewSet, FollowingViewSet, GetCommentsLikes, GetPostsComments, GetPostsLikes, GetUserByEmail, GetUsersFollowing, GetUsersIdealData, GetUsersPosts, GetUsersDaysEvents, IdealDataViewSet, PostLikesViewSet, PostViewSet, ProductivityViewSet, UserViewSet
from rest_framework import routers
from userapi.views import likePost

router = routers.DefaultRouter()
router.register('badge', BadgeViewSet)
router.register(r'user/(?P<email>[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+)', GetUserByEmail, 'User')
router.register('user', UserViewSet)
router.register(r'event/(?P<userID>\d+)/(?P<timestamp>\w+)', GetUsersDaysEvents, 'Event')
router.register('event', EventViewSet)
router.register('post', PostViewSet)
router.register('postLikes', PostLikesViewSet)
router.register('comment', CommentViewSet)
router.register('commentLikes', CommentLikesViewSet)
router.register(r'userFollowing/(?P<userID>\d+)', GetUsersFollowing, 'Following')
router.register(r'userPosts/(?P<userID>\d+)', GetUsersPosts, 'Post')
router.register(r'postLikes/(?P<postID>\d+)', GetPostsLikes, 'PostLikes')
router.register(r'postComments/(?P<postID>\d+)', GetPostsComments, 'Comment')
router.register(r'commentLikes/(?P<commentID>\d+)', GetCommentsLikes, 'CommentLikes')
router.register('following', FollowingViewSet)
router.register('idealData', IdealDataViewSet)
router.register(r'userIdealData/(?P<userID>\d+)', GetUsersIdealData, 'IdealData')
# router.register('productivity', ProductivityViewSet)
# router.register(r'likePost/(?P<postID>\d+)&(?P<userID>\d+)', likePost, 'like_post')

# create: POST - http://localhost:8000/api/user/ with data
# read: GET - http://localhost:8000/api/user/ to get all users, http://localhost:8000/api/user/:userID to get one user
# update: PUT - http://localhost:8000/api/user/:userID/
# delete: DEL - http://localhost:8000/api/user/:userID/

# create: POST - http://localhost:8000/api/event/ with data
# read: GET - http://localhost:8000/api/event/ to get all users, http://localhost:8000/api/event/:eventID to get one user
# update: PUT - http://localhost:8000/api/event/:eventID/
# delete: DEL - http://localhost:8000/api/event/:eventID/