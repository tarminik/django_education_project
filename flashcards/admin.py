from django.contrib import admin
from .models import Language, Lesson, VocabularyItem, Flashcard

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'created_at', 'word_count')
    list_filter = ('language', 'created_at')
    search_fields = ('title', 'description')

@admin.register(VocabularyItem)
class VocabularyItemAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'lesson')
    list_filter = ('lesson', 'created_at')
    search_fields = ('word', 'translation')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('vocabulary_item', 'last_reviewed', 'mastery_level')
    list_filter = ('mastery_level', 'last_reviewed')
    search_fields = ('vocabulary_item__word', 'vocabulary_item__translation')
