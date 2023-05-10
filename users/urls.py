from django.urls import path
from .views import UserView, FriendRequestView, FriendRequestStatusView, FriendsListView, AcceptDeclineView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('friend-requests/', FriendRequestView.as_view()),
    path('friend-requests/<int:user_id>', FriendRequestView.as_view()),
    path('friend-request-status/<int:sender_id>/<int:receiver_id>/', FriendRequestStatusView.as_view()),
    path('friends/<int:user_id>/', FriendsListView.as_view()),
    path('friend-request-action/', AcceptDeclineView.as_view()),
]