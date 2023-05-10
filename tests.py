import requests
import json

base_url = 'http://localhost:8000/users/'

def test_user_creation():
    username = 'testuser1'
    response = requests.post(f'{base_url}users/', data={'username': username})
    print(response.text)

def test_send_friend_request():
    sender_id = 1
    receiver_id = 2
    response = requests.post(f'{base_url}friend-requests/', data={'sender_id': sender_id, 'receiver_id': receiver_id})
    print(response.text)

def test_get_friend_request():
    user_id = 1
    response = requests.get(f'{base_url}friend-requests/{user_id}')
    print(response.text)

def test_friend_request_status():
    sender_id = 1
    receiver_id = 2
    response = requests.get(f'{base_url}friend-request-status/{sender_id}/{receiver_id}/')
    print(response.text)

def test_get_friends():
    user_id = 1
    response = requests.get(f'{base_url}friends/{user_id}/')
    print(response.text)

def test_accept_decline():
    friend_request_id = 1
    action = 'accept'
    response = requests.post(f'{base_url}friend-request-action/', data={'friend_request_id': friend_request_id, 'action': action})
    print(response.text)

if __name__ == "__main__":
    test_user_creation()
    test_send_friend_request()
    test_get_friend_request()
    test_friend_request_status()
    test_get_friends()
    test_accept_decline()
