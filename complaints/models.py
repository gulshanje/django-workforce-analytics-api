from django.db import models

class Complaint(models.Model):
    employee_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default="open")
    priority = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)