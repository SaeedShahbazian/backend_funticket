from django.contrib import admin
from media.models import Image, Video
from django.utils.safestring import mark_safe


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'uuid']
    list_display = [
        "id",
        "desktop_preview",
        "uuid",
        "desktop_url",
        "mobile_url",
    ]

    def desktop_preview(self, obj):
        return mark_safe(u'''<a href="%s" target="_blank">%s</a>''' % (
            obj.desktop.url, obj.desktop.url)
        )

    def mobile_preview(self, obj):
        return mark_safe(u'''<a href="%s" target="_blank">%s</a>''' % (
            obj.mobile.url, obj.mobile.url)
        )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['id', 'uuid']
    list_display = [
        "id",
        "desktop_preview",
        "uuid",
        "desktop_url",
        "mobile_url",
    ]

    def desktop_preview(self, obj):
        return mark_safe(u'''<a href="%s" target="_blank"><img height="30px" src="%s" /></a>''' % (
            obj.desktop.url, obj.desktop.url)
        )

    def mobile_preview(self, obj):
        return mark_safe(u'''<a href="%s" target="_blank"><img height="30px" src="%s" /></a>''' % (
            obj.mobile.url, obj.mobile.url)
        )
