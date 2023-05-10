from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Friendship

class UserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(username=username)
        if created:
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        friends = user.get_friends()
        incoming_requests = user.get_incoming_requests()
        outgoing_requests = user.get_outgoing_requests()
        serialized_friends = []
        serialized_incoming_requests = []
        serialized_outgoing_requests = []
        for friend in friends:
            if ({"id": friend.id, "username": friend.username}) not in serialized_friends:
                serialized_friends.append({"id": friend.id, "username": friend.username})
        for request in incoming_requests:
            serialized_incoming_requests.append({"req_id": request.id, "username": request.sender.username})
        for request in outgoing_requests:
            serialized_outgoing_requests.append({"req_id": request.id, "username": request.receiver.username})
        return Response({"friends": serialized_friends, "incoming_requests": serialized_incoming_requests, "outgoing_requests": serialized_outgoing_requests}, status=status.HTTP_200_OK)

    def post(self, request):
        sender_id = request.data.get('sender_id')
        receiver_id = request.data.get('receiver_id')

        if not sender_id or not receiver_id:
            return Response({"error": "Both sender and receiver ids are required"}, status=status.HTTP_400_BAD_REQUEST)

        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        try:
            sender.send_friend_request(receiver)
            return Response({"message": "Friend request sent successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        sender_id = request.data.get('sender_id')
        receiver_id = request.data.get('receiver_id')

        if not sender_id or not receiver_id:
            return Response({"error": "Both sender and receiver ids are required"}, status=status.HTTP_400_BAD_REQUEST)

        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        try:
            sender.remove_friend(receiver)
            return Response({"message": "Friend removed successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestStatusView(APIView):
    def get(self, request, sender_id, receiver_id):
        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        status_reg = sender.get_friendship_status(receiver)
        return Response({"status": status_reg}, status=status.HTTP_200_OK)

class FriendsListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        friends = []
        for friend in user.get_friends():
            if friend.username not in friends:
                friends.append(friend.username)
        return Response({"friends": friends}, status=status.HTTP_200_OK)

class AcceptDeclineView(APIView):
    def post(self, request):
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')

        if not friend_request_id or not action:
            return Response({"error": "Both friend request id and action are required"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = get_object_or_404(Friendship, id=friend_request_id)

        if action == "accept":
            try:
                friend_request.accept()
                return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif action == "decline":
            try:
                friend_request.decline()
                return Response({"message": "Friend request declined"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)