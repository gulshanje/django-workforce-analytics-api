from django.db import models

class Attendance(models.Model):
    employee_id = models.IntegerField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Employee {self.employee_id} - {self.check_in.date()}"