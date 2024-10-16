from django.contrib import admin

# Register your models here.
from comment.models import Comment, Thread
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['text', 'user__phone_number', 'user__full_name']
    autocomplete_fields = ['user', 'thread', 'parent', 'reviewed_by', 'likes', 'dislikes']
    list_display = [
        "id",
        "user",
        "thread",
        "parent",
        "created_at",
        "modified_at",
        'state'
    ]


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    search_fields = ["id", "type"]
    list_display = [
        "id",
        "type",
        "created_at",
        "modified_at"
    ]
