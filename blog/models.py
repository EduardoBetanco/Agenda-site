from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    due_date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)

    def mark_done(self):
        self.status = True
        self.save()

    def mark_undone(self):
        self.status = False
        self.save()

    def __str__(self):
        return self.title