# models.py
from django.db import models
from datetime import date
from django.utils import timezone

# Admin/User data
class SignupData(models.Model):
    username = models.CharField(max_length=30, unique=True)
    organization = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

# Events created by admin
class Events(models.Model):
    user = models.ForeignKey(SignupData, on_delete=models.CASCADE, related_name='events', null=True)
    event = models.CharField(max_length=100, verbose_name="Event Title")
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    type = models.CharField(max_length=30, default="Program", verbose_name="Event Type")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    available = models.IntegerField(null=True, blank=True)
    venue = models.CharField(max_length=100, default='TBD')
    Money = models.IntegerField(null=True, blank=True)
    for_class = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.event} ({self.start_date})"

    # ✅ Dynamic status method
    def status(self):
        today = date.today()
        if today < self.start_date:
            return "Start Soon"
        elif self.start_date <= today <= self.end_date:
            return "Ongoing"
        else:
            return "Ended"

class Students(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    student_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    class_level = models.IntegerField(null=True, blank=True)
    faculty = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Booking(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="bookings")
    student_name = models.CharField(max_length=50, default="Unknown Student")
    event_id_ref = models.IntegerField(default=1)
    booked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.first_name} booked {self.event.event}"