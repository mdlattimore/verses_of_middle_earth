from django.contrib import admin
from .models import Verse, Character, Place
# Register your models here.

class VerseAdmin(admin.ModelAdmin):
    list_filter = ["book",]
    list_display = ("book", "get_speakers", "short_text")
    filter_horizontal = ('speaker',)
    ordering = ("book", "sub_book", "chapter", "page",)
    readonly_fields = ('id',)

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    
    # This method will return a comma-separated list of authors for each book
    def get_speakers(self, obj):
        return ", ".join([character.name for character in obj.speaker.all()])
    
    get_speakers.short_description = "Speaker(s)"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.distinct()  # Ensure each book appears only once


class CharacterAdmin(admin.ModelAdmin):
    list_filter = ['name', 'race']
    list_display = ('name', 'race')
    ordering = ('name',)
    readonly_fields = ('id',)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    readonly_fields = ('id',)

admin.site.register(Verse, VerseAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Place, PlaceAdmin)
