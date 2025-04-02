from django import forms
from .models import Language, Lesson, VocabularyItem, Flashcard

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }

class VocabularyItemForm(forms.ModelForm):
    class Meta:
        model = VocabularyItem
        fields = ['word', 'translation', 'example_sentence', 'lesson', 'image']
        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control'}),
            'translation': forms.TextInput(attrs={'class': 'form-control'}),
            'example_sentence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lesson': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FlashcardBatchUploadForm(forms.Form):
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    csv_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file')
        return csv_file
