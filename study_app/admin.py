from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
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
    # KEEP the change_list_template for the change list page
    change_list_template = "admin/study_app/quizquestion_change_list.html"
    # ADD custom template for add form
    add_form_template = "admin/study_app/quizquestion_add_form.html"
    
    list_display = ['book', 'module', 'chapter', 'question_text_short', 'verse_reference']
    list_filter = ['book', 'module', 'chapter']
    search_fields = ['question_text', 'prabhupada_commentary', 'verse_reference']
    ordering = ['module', 'chapter', 'order']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-paste-questions/', self.admin_site.admin_view(self.bulk_paste_questions)),
        ]
        return custom_urls + urls
    
    def bulk_paste_questions(self, request):
        if request.method == 'POST':
            questions_text = request.POST.get('questions_text', '').strip()
            book_id = request.POST.get('book')
            module_id = request.POST.get('module')
            chapter = request.POST.get('chapter', 'Chapter 1')
            
            if questions_text and book_id and module_id:
                try:
                    book = Book.objects.get(id=book_id)
                    module = QuizModule.objects.get(id=module_id)
                    
                    # BETTER SPLITTING: Handle various line endings and empty lines
                    questions_list = []
                    for line in questions_text.splitlines():
                        line = line.strip()
                        if line:  # Only non-empty lines
                            questions_list.append(line)
                    
                    created_count = 0
                    for i, question_text in enumerate(questions_list, start=1):
                        # Skip if question already exists
                        if not QuizQuestion.objects.filter(
                            book=book, 
                            module=module, 
                            question_text=question_text
                        ).exists():
                            
                            QuizQuestion.objects.create(
                                book=book,
                                module=module,
                                chapter=chapter,
                                question_text=question_text,
                                order=i
                            )
                            created_count += 1
                    
                    if created_count > 0:
                        messages.success(request, f'Successfully created {created_count} new questions!')
                    else:
                        messages.warning(request, 'No new questions created. They may already exist.')
                        
                    return redirect('admin:study_app_quizquestion_changelist')
                    
                except (Book.DoesNotExist, QuizModule.DoesNotExist):
                    messages.error(request, 'Invalid book or module selected.')
        
        # GET request - show the form
        books = Book.objects.all()
        modules = QuizModule.objects.all()
        context = {
            'books': books,
            'modules': modules,
            'title': 'Bulk Upload Questions'
        }
        return render(request, 'admin/study_app/bulk_paste_form.html', context)
    
    def question_text_short(self, obj):
        return obj.question_text[:100] + '...' if len(obj.question_text) > 100 else obj.question_text
    question_text_short.short_description = 'Question Text'

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'score', 'completed_at']
    list_filter = ['module', 'completed_at']
    readonly_fields = ['completed_at', 'score', 'total_questions']
    ordering = ['-completed_at']
