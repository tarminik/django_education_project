from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Lesson URLs
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/new/', views.LessonCreateView.as_view(), name='lesson-create'),
    
    # Vocabulary URLs
    path('vocabulary/', views.VocabularyListView.as_view(), name='vocabulary-list'),
    path('vocabulary/new/', views.VocabularyCreateView.as_view(), name='vocabulary-create'),
    
    # Flashcard URLs
    path('flashcards/', views.flashcard_list, name='flashcard-list'),
    path('flashcards/study/', views.flashcard_study, name='flashcard-study'),
    path('flashcards/upload/', views.flashcard_batch_upload, name='flashcard-batch-upload'),
    path('flashcards/<int:pk>/update-mastery/', views.update_flashcard_mastery, name='update-flashcard-mastery'),
]
