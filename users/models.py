from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)

    def send_friend_request(self, to_user):
        if to_user != self:
            friendship, created = Friendship.objects.get_or_create(sender=self, receiver=to_user)
            if created:
                mutual_request = Friendship.objects.filter(sender=to_user, receiver=self, status=Friendship.STATUS_PENDING).first()
                if mutual_request:
                    friendship.accept()
                    mutual_request.accept()
            else:
                raise ValueError("Friendship already requested")
        else:
            raise ValueError("Cannot send friend request to self")

    def remove_friend(self, friend):
        Friendship.objects.filter(
            Q(sender=self, receiver=friend, status=Friendship.STATUS_ACCEPTED) |
            Q(receiver=self, sender=friend, status=Friendship.STATUS_ACCEPTED)).delete()

    def get_friendship_status(self, other_user):
        if Friendship.objects.filter(sender=self, receiver=other_user, status=Friendship.STATUS_ACCEPTED).exists():
            return "friends"
        elif Friendship.objects.filter(sender=other_user, receiver=self, status=Friendship.STATUS_ACCEPTED).exists():
            return "friends"
        elif Friendship.objects.filter(sender=self, receiver=other_user, status=Friendship.STATUS_PENDING).exists():
            return "has outgoing"
        elif Friendship.objects.filter(receiver=self, sender=other_user, status=Friendship.STATUS_PENDING).exists():
            return "has incoming"
        else:
            return "nothing"

    def get_friends(self):
        friends = []
        sent_friendships = self.sent_friend_requests.filter(status=Friendship.STATUS_ACCEPTED)
        received_friendships = self.received_friend_requests.filter(status=Friendship.STATUS_ACCEPTED)
        for friendship in sent_friendships:
            friends.append(friendship.receiver)
        for friendship in received_friendships:
            if friendship not in sent_friendships:
                friends.append(friendship.sender)
        return friends

    def get_incoming_requests(self):
        return self.received_friend_requests.filter(status=Friendship.STATUS_PENDING)

    def get_outgoing_requests(self):
        return self.sent_friend_requests.filter(status=Friendship.STATUS_PENDING)


class Friendship(models.Model):
    STATUS_PENDING = 0
    STATUS_ACCEPTED = 1

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
    )

    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            raise ValueError("Cannot friend yourself")
        super(Friendship, self).save(*args, **kwargs)

    def accept(self):
        if self.status == Friendship.STATUS_PENDING:
            self.status = Friendship.STATUS_ACCEPTED
            self.save()
        else:
            raise ValueError("Cannot accept a non-pending request")

    def decline(self):
        if self.status == Friendship.STATUS_PENDING:
            self.delete()
        else:
            raise ValueError("Cannot decline a non-pending request")
