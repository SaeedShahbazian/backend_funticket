from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from reversion.admin import VersionAdmin
from users.models import User, Message


@admin.register(User)
class UserAdmin(VersionAdmin, BaseUserAdmin):
    autocomplete_fields = [
        'city',
    ]
    search_fields = ['id', 'username', 'phone_number', 'email', 'city__name_fa', 'city__name_en', 'full_name']
    list_display = ('username', 'phone_number', 'avatar', 'email', 'city', 'date_joined', 'is_staff')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'user',
        'message_sender'
    ]
    search_fields = ['id', 'user__username', 'user__phone_number', 'user__email', 'user__full_name', 'message_content', 'title']
    list_display = ('id', 'user', 'title', 'message_content', 'image', 'read', 'created_at', 'message_sender')
