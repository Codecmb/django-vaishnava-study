#!/usr/bin/env python3
admin_content = '''from django.contrib import admin
from .models import QuizQuestion, QuizModule, Book, Course, QuestionAnswer, StudyMaterial

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'book', 'module', 'chapter', 'order']
    list_filter = ['book', 'module', 'chapter']
    search_fields = ['question_text', 'correct_answers', 'verse_reference']
    list_editable = ['chapter', 'order']
    list_per_page = 50
    
    fieldsets = [
        ('Basic Info', {
            'fields': ['book', 'module', 'chapter', 'order']
        }),
        ('Question Content', {
            'fields': [
                'question_text',
                'multiple_choice_options',
                'correct_answers',
                'prabhupada_commentary',
                'additional_guidance', 
                'verse_reference'
            ]
        }),
    ]

class QuizModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'chapters_range', 'order']
    list_filter = ['course']
    list_editable = ['order']
    search_fields = ['name', 'chapters_range']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    list_editable = ['order']
    search_fields = ['title']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'order']
    list_editable = ['order']
    list_filter = ['level']

admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizModule, QuizModuleAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(QuestionAnswer)
admin.site.register(StudyMaterial)
'''

with open('study_app/admin.py', 'w') as f:
    f.write(admin_content)

print('✅ Created admin.py configuration')
