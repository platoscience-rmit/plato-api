from django.db import models

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text Input'),
        ('radio', 'Radio Button'),
        ('select', 'Dropdown Select'),
        ('checkbox', 'Checkbox'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='text')
