from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='courses/')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')  # ⭐ prevents duplicate



# Live class



class LiveClass(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('ended', 'Ended'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='live_classes/thumbnails/', blank=True, null=True)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    enable_chat = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.title} — {self.scheduled_at.strftime('%d %b %Y %H:%M')}"

    @property
    def youtube_live_embed_url(self):
        # ✅ Always points to current live — no video ID needed
        channel_id = settings.YOUTUBE_CHANNEL_ID
        return f"https://www.youtube.com/embed/live_stream?channel={channel_id}&autoplay=1"

    @property
    def youtube_live_watch_url(self):
        # ✅ Opens YouTube live page directly
        channel_id = settings.YOUTUBE_CHANNEL_ID
        return f"https://www.youtube.com/channel/{channel_id}/live"

    @property
    def youtube_chat_url(self):
        # ✅ Live chat via channel
        channel_id = settings.YOUTUBE_CHANNEL_ID
        return f"https://www.youtube.com/live_chat?is_popout=1&embed_domain=yourdomain.com&v=live_stream&channel={channel_id}"

    @property
    def is_live_now(self):
        return self.status == 'live'


class RecordedReplay(models.Model):
    live_class = models.OneToOneField(
        LiveClass, on_delete=models.CASCADE, related_name='replay'
    )
    # ✅ After class ends, paste the specific recorded video ID here
    youtube_video_id = models.CharField(max_length=50)
    recorded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Replay: {self.live_class.title}"

    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_video_id}?rel=0"

    @property
    def watch_url(self):
        # ✅ Opens recorded video on YouTube
        return f"https://www.youtube.com/watch?v={self.youtube_video_id}"