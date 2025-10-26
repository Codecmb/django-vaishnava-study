from django.contrib import admin
<<<<<<< Updated upstream
import csv
from django.http import HttpResponse
from .models import Course, Book, StudyMaterial, QuestionAnswer, QAUpload, QuizModule, QuizQuestion, QuizAttempt
=======
from .models import QuizQuestion, QuizModule, Book, Course, QuestionAnswer, StudyMaterial
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['book', 'verse_reference', 'order']
    list_filter = ['book']
    ordering = ['book', 'order']

@admin.register(QAUpload)
class QAUploadAdmin(admin.ModelAdmin):
    list_display = ['book', 'uploaded_at', 'processed']
    list_filter = ['processed', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(QuizModule)
class QuizModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'chapters_range', 'order']
    list_filter = ['course']
    ordering = ['course', 'order']
    actions = ['duplicate_quiz', 'export_questions']
    
    def duplicate_quiz(self, request, queryset):
        """Duplicate selected quizzes"""
        for quiz in queryset:
            quiz.pk = None
            quiz.name += " (Copy)"
            quiz.save()
        self.message_user(request, f"Duplicated {queryset.count()} quizzes")
    
    def export_questions(self, request, queryset):
        """Export questions to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quiz_questions.csv"'
        writer = csv.writer(response)
        writer.writerow(['Module', 'Verse Reference', 'Question'])
        for module in queryset:
            for question in module.quizquestion_set.all():
                writer.writerow([module.name, question.verse_reference, question.question_text])
        return response

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['book', 'module', 'chapter', 'question_text_short', 'verse_reference']
    list_filter = ['book', 'module', 'chapter']
    search_fields = ['question_text', 'prabhupada_commentary', 'verse_reference']
    ordering = ['module', 'chapter', 'order']
    actions = ['delete_duplicates']
    
    def question_text_short(self, obj):
        return obj.question_text[:75] + "..." if len(obj.question_text) > 75 else obj.question_text
    question_text_short.short_description = 'Question'
    
    def delete_duplicates(self, request, queryset):
        """Delete duplicate questions"""
        seen = set()
        deleted = 0
        for question in queryset.order_by('id'):
            key = (question.module_id, question.verse_reference, question.question_text)
            if key in seen:
                question.delete()
                deleted += 1
            else:
                seen.add(key)
        self.message_user(request, f"Deleted {deleted} duplicate questions")

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'module', 'score', 'total_questions', 'completed_at']
    list_filter = ['book', 'module', 'completed_at']
    readonly_fields = ['completed_at']
    ordering = ['-completed_at']

# Debug - remove after testing
=======
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizModule, QuizModuleAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(QuestionAnswer)
admin.site.register(StudyMaterial)
>>>>>>> Stashed changes
