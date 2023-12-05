from django.contrib import admin
from .models import Quest, Location

class LocationInline(admin.TabularInline):
    model = Location
    extra = 3

class QuestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [LocationInline]
    list_display = ["title", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["title"]

admin.site.register(Quest, QuestAdmin)