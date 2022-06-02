from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "public", "importance", "condition", "date_and_time", "id")

    # fields =
    # readonly_fields =

    search_fields = ['title', "message"]

    list_filter = ('public', 'importance',)

# Register your models here.

