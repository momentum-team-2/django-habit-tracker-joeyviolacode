from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from users.models import User
from datetime import date, timedelta
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

    def get_record_details(self):
        records = list(self.records.filter(date__gte=date.today()-timedelta(30)).order_by("date").values("date", "is_met", "number", "id")) 
        days = []
        today = date.today()
        if len(records) == 0:   #set start date for list of dates
            start = today
        else:
            start = records[0]['date']
        while start <= today:   #make list of dates from start date until today
            days.append(start)
            start += timedelta(1)
        record_list = []
        for day in days:
            if len(records) > 0:
                if day == records[0]['date']:
                    record_list.append({"date": day, "is_met" : records[0]["is_met"], "number": records[0]["number"], "pk":  records[0]["id"]})
                    records = records[1:]
                else:
                    record_list.append( {"date": day, "is_met" : None, "number": None, "pk": None})
            else:
                record_list.append( {"date": day, "is_met" : None, "number": None, "pk": None})
        return record_list
        
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

    def get_dict(self):
        return { "date": self.date, "is_met": self.is_met, "number": self.number }