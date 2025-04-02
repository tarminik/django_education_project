from django.db import models
from django.core.validators import MinLengthValidator

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def word_count(self):
        return self.vocabulary_items.count()

class VocabularyItem(models.Model):
    word = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    translation = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    example_sentence = models.TextField(blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='vocabulary_items')
    image = models.ImageField(upload_to='vocabulary_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.word} - {self.translation}"

class Flashcard(models.Model):
    vocabulary_item = models.OneToOneField(VocabularyItem, on_delete=models.CASCADE, related_name='flashcard')
    last_reviewed = models.DateTimeField(blank=True, null=True)
    mastery_level = models.IntegerField(default=0)  # 0-5 scale of mastery
    
    def __str__(self):
        return f"Flashcard: {self.vocabulary_item.word}"
