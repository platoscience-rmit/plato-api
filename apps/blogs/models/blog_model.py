from django.db import models

class Blog(models.Model):
    
    title = models.TextField()
    author = models.TextField()
    read_time = models.IntegerField()
    published_data = models.DateTimeField()
    status = models.BooleanField()
    is_popular = models.BooleanField()
    cover_image = models.CharField()
    author_avatar = models.CharField()
    
    