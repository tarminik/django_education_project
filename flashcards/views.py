import csv
import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Language, Lesson, VocabularyItem, Flashcard
from .forms import LanguageForm, LessonForm, VocabularyItemForm, FlashcardBatchUploadForm

# Home page view
def home(request):
    lessons = Lesson.objects.all().order_by('-created_at')[:5]
    languages = Language.objects.all()
    vocab_count = VocabularyItem.objects.count()
    flashcard_count = Flashcard.objects.count()
    
    context = {
        'lessons': lessons,
        'languages': languages,
        'vocab_count': vocab_count,
        'flashcard_count': flashcard_count,
    }
    return render(request, 'flashcards/home.html', context)

# Lesson views
class LessonListView(ListView):
    model = Lesson
    template_name = 'flashcards/lesson_list.html'
    context_object_name = 'lessons'
    ordering = ['-created_at']

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'flashcards/lesson_detail.html'
    context_object_name = 'lesson'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vocabulary_items'] = self.object.vocabulary_items.all()
        return context

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'flashcards/lesson_form.html'
    success_url = reverse_lazy('lesson-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Lesson created successfully!')
        return super().form_valid(form)

# Vocabulary views
class VocabularyListView(ListView):
    model = VocabularyItem
    template_name = 'flashcards/vocabulary_list.html'
    context_object_name = 'vocabulary_items'
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        lesson_id = self.request.GET.get('lesson')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.all()
        context['current_lesson'] = self.request.GET.get('lesson')
        return context

class VocabularyCreateView(CreateView):
    model = VocabularyItem
    form_class = VocabularyItemForm
    template_name = 'flashcards/vocabulary_form.html'
    success_url = reverse_lazy('vocabulary-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Automatically create a flashcard for this vocabulary item
        Flashcard.objects.create(vocabulary_item=self.object)
        messages.success(self.request, 'Vocabulary item and flashcard created successfully!')
        return response

# Flashcard views
def flashcard_list(request):
    flashcards = Flashcard.objects.all().select_related('vocabulary_item')
    return render(request, 'flashcards/flashcard_list.html', {'flashcards': flashcards})

def flashcard_study(request):
    flashcards = Flashcard.objects.all().select_related('vocabulary_item')
    return render(request, 'flashcards/flashcard_study.html', {'flashcards': flashcards})

def flashcard_batch_upload(request):
    if request.method == 'POST':
        form = FlashcardBatchUploadForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.cleaned_data['lesson']
            csv_file = request.FILES['csv_file']
            
            # Process CSV file
            csv_data = csv_file.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(csv_data))
            next(csv_reader, None)  # Skip header row
            
            count = 0
            for row in csv_reader:
                if len(row) >= 2:  # Ensure we have at least word and translation
                    word, translation = row[0], row[1]
                    example = row[2] if len(row) > 2 else ''
                    
                    # Create vocabulary item and flashcard
                    vocab_item = VocabularyItem.objects.create(
                        word=word,
                        translation=translation,
                        example_sentence=example,
                        lesson=lesson
                    )
                    Flashcard.objects.create(vocabulary_item=vocab_item)
                    count += 1
            
            messages.success(request, f'Successfully imported {count} vocabulary items and flashcards!')
            return redirect('vocabulary-list')
    else:
        form = FlashcardBatchUploadForm()
    
    return render(request, 'flashcards/flashcard_batch_upload.html', {'form': form})

def update_flashcard_mastery(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    
    if request.method == 'POST':
        mastery_level = int(request.POST.get('mastery_level', 0))
        if 0 <= mastery_level <= 5:
            flashcard.mastery_level = mastery_level
            flashcard.last_reviewed = datetime.now()
            flashcard.save()
            return HttpResponse(status=200)
    
    return HttpResponse(status=400)
