from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Rule


@admin.register(Rule)
class RuleAdmin(ModelAdmin):
    list_display = ("id", "name", "trigger", "action", "priority", "is_enabled", "updated_at")
    list_filter = ("is_enabled", "trigger", "action")
    search_fields = ("name", "trigger", "condition", "action")
    ordering = ("priority", "-updated_at")
    list_editable = ("priority", "is_enabled")
