import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # Extends User model
    completed_quests = models.ManyToManyField('Quest', related_name='completed_by', blank=True)
    completed_locations = models.ManyToManyField('Location', related_name='completed_by', blank=True)
    liked_quests = models.ManyToManyField('Quest', related_name='liked_by', blank=True)
    rated_quests = models.ManyToManyField('Quest', related_name='rated_by', blank=True)

class Author(models.Model):
    name = models.CharField(max_length=100, default="anonymous")
    email = models.EmailField()
    quests_complete = models.PositiveIntegerField(default=0)
    quests_created = models.PositiveIntegerField(default=0)
    
class Quest(models.Model):
    CACHE_TYPE_CHOICES = [
        ('Traditional', 'Traditional'),
        ('Event', 'Event'),
        ('Virtual', 'Virtual'),
        ('Locationless', 'Locationless'),
    ]

    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    feedback = models.CharField(max_length=500, default="Pending approval.")
    likes = models.PositiveIntegerField(default=0)
    difficulty = models.DecimalField(default=0, decimal_places=2, max_digits=3)
    num_ratings = models.PositiveIntegerField(default=0)
    ratings_total = models.PositiveIntegerField(default=0)
    cache_type = models.CharField(
        max_length=20,
        choices=CACHE_TYPE_CHOICES,
        default='Traditional'
    )

    def __str__(self):
        return self.title
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
class Location(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400, default="")
    clue = models.CharField(max_length=200, default="")
    answer = models.CharField(max_length=200, default="")
    lat = models.DecimalField(decimal_places=14, max_digits=17)
    long = models.DecimalField(decimal_places=14, max_digits=17)

    def __str__(self):
        return self.title