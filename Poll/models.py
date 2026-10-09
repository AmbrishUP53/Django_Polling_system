from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Polls(models.Model):
    title = models.CharField(max_length=200)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    candidates = models.ManyToManyField(
        Candidate,
        related_name='Polls'
    )
    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    candidate=models.ForeignKey(Candidate , on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls , on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta :
        constraints = [
            models.UniqueConstraint(
                fields=['user' ,'poll'],
                name="one_vote_per_user_per_poll"
            )
        ]
    def __str__(self):
        return f"{self.user.username}-{self.candidate.name}"