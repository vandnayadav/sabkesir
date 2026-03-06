from django.contrib import admin
from .models import LiveClass, RecordedReplay
from .models import Course

admin.site.register(Course)


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'subject', 'scheduled_at', 'status', 'is_free']
    list_filter = ['status', 'subject', 'is_free']
    search_fields = ['title', 'instructor', 'subject']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Class Info', {
            'fields': ('title', 'description', 'instructor', 'subject', 'thumbnail', 'is_free')
        }),
        ('Schedule', {
            'fields': ('scheduled_at', 'duration_minutes', 'status')
        }),
        # ✅ Removed youtube_video_id — now using channel ID from settings.py
        ('Chat Settings', {
            'fields': ('enable_chat',),
            'description': 'YouTube channel ID is set globally in settings.py — no video ID needed per class.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RecordedReplay)
class RecordedReplayAdmin(admin.ModelAdmin):
    list_display = ['live_class', 'recorded_at', 'views']
    search_fields = ['live_class__title']
    readonly_fields = ['recorded_at']
    fieldsets = (
        ('Replay Info', {
            'fields': ('live_class', 'youtube_video_id', 'views'),
            'description': 'Paste the specific YouTube video ID of the recorded class here after the session ends.'
        }),
        ('Timestamps', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )