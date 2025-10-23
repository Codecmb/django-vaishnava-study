from django.contrib import admin
from .models import Course, Book, StudyMaterial, QuestionAnswer, QAUpload, QuizModule, QuizQuestion, QuizAttempt

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'order']
    list_filter = ['level']
    ordering = ['order']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    ordering = ['course', 'order']

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'material_type', 'language', 'order']
    list_filter = ['material_type', 'language', 'book']
    ordering = ['book', 'order']

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

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['book', 'module', 'chapter', 'question_text_short', 'verse_reference']
    list_filter = ['book', 'module', 'chapter']
    search_fields = ['question_text', 'prabhupada_commentary', 'verse_reference']
    ordering = ['module', 'chapter', 'order']
    
    def question_text_short(self, obj):
        return obj.question_text[:75] + "..." if len(obj.question_text) > 75 else obj.question_text
    question_text_short.short_description = 'Question'

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'module', 'score', 'total_questions', 'completed_at']
    list_filter = ['book', 'module', 'completed_at']
    readonly_fields = ['completed_at']
    ordering = ['-completed_at']
