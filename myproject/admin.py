from django.contrib import admin
from django.contrib.admin import ModelAdmin

from myproject.models import Entry, Vote, Edition


class EntryAdmin(ModelAdmin):
    list_display = ('code', 'title')
    pass

class VoteAdmin(ModelAdmin):
    list_display = ('voter', 'entry', 'score')
    search_fields = ('voter', 'entry__title', 'entry__code')
    pass

class EditionAdmin(ModelAdmin):
    list_display = ('name', 'year')
    pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Edition, EditionAdmin)