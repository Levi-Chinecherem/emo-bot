from django.contrib import admin
from .models import Comment, LogEntry, UserInteraction

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    list_display_links = ('id', 'text')
    list_filter = ('created_at',)
    search_fields = ('text',)

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'command', 'message')
    list_display_links = ('timestamp', 'command')
    list_filter = ('timestamp', 'command')
    search_fields = ('message',)

class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ('id', 'text')
    search_fields = ('text',)

# Register your models with the custom admin classes
admin.site.register(Comment, CommentAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(UserInteraction, UserInteractionAdmin)
