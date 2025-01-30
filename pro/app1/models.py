from django.db import models

class SpeedRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    track_id = models.IntegerField()
    class_name = models.CharField(max_length=255)
    speed = models.FloatField()
    numberplate = models.TextField()

    def __str__(self):
        return f"Track ID: {self.track_id}, Speed: {self.speed} km/h"
