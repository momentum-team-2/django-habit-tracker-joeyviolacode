from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from users.models import User
# Create your models here.

class Habit(models.Model):
    verb = models.CharField(max_length = 20)
    noun = models.CharField(max_length = 20)
    noun_singular = models.CharField(max_length = 20)
    number = models.FloatField()
    is_negative = models.BooleanField(default=False)
    created_date = models.DateField()
    user = models.ForeignKey(User, related_name="habits", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.verb} {self.noun} {self.number}"


class Record(models.Model):
    number = models.FloatField()
    is_met = models.BooleanField(default = False)
    habit = models.ForeignKey(Habit, related_name="records", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="records", on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'user', 'date'], name='unique_record')
        ]
 
    def __str__(self):
        return f"{self.user} {self.habit} {self.date}"