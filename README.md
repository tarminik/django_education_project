# LinguaLearn - Language Learning Platform

A Django-based educational web application for language learning with flashcards, vocabulary management, and lessons.

## Features

- **Lessons Management**: Create and organize language lessons
- **Vocabulary Management**: Add words with translations, example sentences, and images
- **Flashcard System**: Study vocabulary with interactive flashcards
- **Batch Upload**: Import multiple vocabulary items at once via CSV

## Requirements

- Python 3.x
- Django 3.2+
- Pillow (for image handling)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`

## Usage

1. Access the admin panel at `/admin/` to add languages
2. Create lessons and add vocabulary items
3. Use the flashcard system to study and track your progress
