from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Vote.models import VotingItem, VoteEvent

admin.site.register(VoteEvent)


@admin.register(VotingItem)
class VotingItemAdmin(ModelAdmin):
    class Media:
        js = (
            '/static/js/load.js',
        )
