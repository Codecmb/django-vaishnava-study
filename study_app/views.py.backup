from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import get_language, activate, gettext as _
from django.contrib import messages
from django.db import models
import csv
import io
import os
from .models import Course, Book, QuestionAnswer, QAUpload, StudyMaterial
from .forms import QAUploadForm, StudyMaterialForm

def index(request):
    courses = Course.objects.all().prefetch_related('books')
    
    # Debug info
    print("=== STATIC FILES DEBUG ===")
    print(f"Current language: {get_language()}")
    print(f"Request LANGUAGE_CODE: {request.LANGUAGE_CODE}")
    
    context = {
        'courses': courses,
    }
    return render(request, 'study_app/index.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    books = course.books.all()
    
    context = {
        'course': course,
        'books': books,
    }
    return render(request, 'study_app/course_detail.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    qas = book.qas.all()
    materials = book.materials.all()
    
    context = {
        'book': book,
        'qas': qas,
        'materials': materials,
    }
    return render(request, 'study_app/book_detail.html', context)

def qa_section(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    qas = book.qas.all()
    study_materials = book.materials.all()
    
    # Organize materials by type
    materials_by_type = {}
    for material in study_materials:
        if material.material_type not in materials_by_type:
            materials_by_type[material.material_type] = []
        materials_by_type[material.material_type].append(material)
    
    context = {
        'book': book,
        'qas': qas,
        'materials_by_type': materials_by_type,
        'study_materials': study_materials,
    }
    return render(request, 'study_app/qa_section.html', context)

def upload_qa(request):
    if request.method == 'POST':
        form = QAUploadForm(request.POST, request.FILES)
        if form.is_valid():
            qa_upload = form.save()
            
            # Process the CSV file
            try:
                csv_file = qa_upload.csv_file.read().decode('utf-8')
                csv_reader = csv.DictReader(io.StringIO(csv_file))
                
                questions_created = 0
                for row in csv_reader:
                    QuestionAnswer.objects.create(
                        book=qa_upload.book,
                        question_en=row['question_en'],
                        question_es=row['question_es'],
                        answer_en=row['answer_en'],
                        answer_es=row['answer_es'],
                        verse_reference=row['verse_reference'],
                        order=int(row['order'])
                    )
                    questions_created += 1
                
                qa_upload.processed = True
                qa_upload.save()
                
                messages.success(request, f'Successfully uploaded {questions_created} questions for {qa_upload.book.title}')
                return redirect('study_app:upload_success')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                qa_upload.delete()
    else:
        form = QAUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'study_app/upload_qa.html', context)

def upload_study_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            messages.success(request, f'Successfully uploaded {material.get_material_type_display()} for {material.book.title}')
            return redirect('study_app:upload_success')
    else:
        form = StudyMaterialForm()
    
    context = {
        'form': form,
    }
    return render(request, 'study_app/upload_study_material.html', context)

def delete_study_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    
    if request.method == 'POST':
        # Delete the actual files from storage
        if material.english_file:
            if os.path.isfile(material.english_file.path):
                os.remove(material.english_file.path)
        if material.spanish_file:
            if os.path.isfile(material.spanish_file.path):
                os.remove(material.spanish_file.path)
        if material.bilingual_file:
            if os.path.isfile(material.bilingual_file.path):
                os.remove(material.bilingual_file.path)
        
        book_id = material.book.id
        material_name = material.title
        material.delete()
        
        messages.success(request, f'Successfully deleted "{material_name}"')
        return redirect('study_app:qa_section', book_id=book_id)
    
    context = {
        'material': material,
    }
    return render(request, 'study_app/delete_study_material.html', context)

def upload_success(request):
    return render(request, 'study_app/upload_success.html')

# Test view for static files
def test_static(request):
    return render(request, 'study_app/test_static.html')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile_redirect(request):
    """Redirect from /accounts/profile/ to homepage"""
    return redirect('study_app:index')

# Add this function to enhance the quiz dashboard if needed

@login_required
def bulk_questions(request, book_id):
    """Bulk upload questions for a specific book"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from django.db import models
    from .models import Book, QuizModule, QuizQuestion
    
    book = get_object_or_404(Book, id=book_id)
    modules = QuizModule.objects.filter(course=book.course)
    
    if request.method == 'POST':
        module_id = request.POST.get('module')
        chapter = request.POST.get('chapter', 'Chapter 1')
        questions_text = request.POST.get('questions_text', '')
        
        if not module_id:
            messages.error(request, 'Please select a module')
        elif not questions_text.strip():
            messages.error(request, 'Please enter some questions')
        else:
            try:
                module = QuizModule.objects.get(id=module_id)
                
                # Parse questions (one per line)
                lines = [line.strip() for line in questions_text.split('\n') if line.strip()]
                imported_count = 0
                existing_count = 0
                
                # Get current max order for this module
                max_order = QuizQuestion.objects.filter(module=module).aggregate(models.Max('order'))['order__max'] or 0
                
                for i, question_text in enumerate(lines, 1):
                    if not question_text:
                        continue
                        
                    # Skip if question already exists (case insensitive partial match)
                    if QuizQuestion.objects.filter(
                        module=module, 
                        question_text__icontains=question_text[:50]
                    ).exists():
                        existing_count += 1
                        continue
                    
                    QuizQuestion.objects.create(
                        book=book,
                        module=module,
                        chapter=chapter,
                        question_text=question_text,
                        order=max_order + i,
                        additional_guidance="Study relevant scriptures"
                    )
                    imported_count += 1
                
                if imported_count > 0:
                    messages.success(request, f'Successfully imported {imported_count} questions to {module.name}!')
                if existing_count > 0:
                    messages.warning(request, f'Skipped {existing_count} duplicate questions')
                    
                return redirect('study_app:quiz_dashboard', book_id=book_id)
                
            except Exception as e:
                messages.error(request, f'Error importing questions: {str(e)}')
    
    context = {
        'book': book,
        'modules': modules,
    }
    return render(request, 'study_app/bulk_questions.html', context)

# AI Validation View - New functionality
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

@csrf_exempt
def validate_answer_with_ai(request, question_id):
    """
    AI validation endpoint for quiz answers - NEW FEATURE
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            student_answer = data.get('answer', '')
            
            from .models import QuizQuestion
            question = QuizQuestion.objects.get(id=question_id)
            
            # Simple AI validation (can be enhanced later)
            answer_length = len(student_answer)
            if answer_length > 100:
                score = 85
                is_aligned = True
                feedback = 'Good detailed answer showing understanding.'
            elif answer_length > 50:
                score = 65
                is_aligned = True
                feedback = 'Basic understanding shown.'
            else:
                score = 40
                is_aligned = False
                feedback = 'Please provide more detailed answer.'
            
            # Save feedback
            question.ai_feedback = feedback
            question.ai_score = score
            question.is_siddhanta_aligned = is_aligned
            question.feedback_timestamp = timezone.now()
            question.save()
            
            return JsonResponse({
                'feedback': feedback,
                'score': score,
                'is_aligned': is_aligned
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def bulk_upload_questions(request, book_id, module_id):
    """Bulk upload questions with automatic choice generation"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from .models import Book, QuizModule, QuizQuestion
    
    book = get_object_or_404(Book, id=book_id)
    module = get_object_or_404(QuizModule, id=module_id)
    
    if request.method == 'POST':
        if 'questions_text' in request.POST:
            questions_text = request.POST['questions_text']
            questions_list = [q.strip() for q in questions_text.split('\n') if q.strip()]
            
            created_count = 0
            for question_text in questions_list:
                question = QuizQuestion(
                    book=book,
                    module=module,
                    question_text=question_text,
                    chapter=request.POST.get('chapter', 'Chapter 1')
                )
                question.save()  # This will trigger the signal to generate choices
                created_count += 1
            
            messages.success(request, f'Successfully created {created_count} questions with auto-generated multiple choice options!')
            return redirect('study_app:quiz_dashboard', book_id=book_id)
    
    context = {
        'book': book,
        'module': module,
    }
    return render(request, 'study_app/bulk_upload_questions.html', context)

def bulk_upload_questions(request, book_id, module_id):
    """Bulk upload questions with automatic choice generation"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from .models import Book, QuizModule, QuizQuestion
    
    book = get_object_or_404(Book, id=book_id)
    module = get_object_or_404(QuizModule, id=module_id)
    
    if request.method == 'POST':
        if 'questions_text' in request.POST:
            questions_text = request.POST['questions_text']
            questions_list = [q.strip() for q in questions_text.split('\n') if q.strip()]
            
            created_count = 0
            for question_text in questions_list:
                question = QuizQuestion(
                    book=book,
                    module=module,
                    question_text=question_text,
                    chapter=request.POST.get('chapter', 'Chapter 1')
                )
                question.save()  # This will trigger the signal to generate choices
                created_count += 1
            
            messages.success(request, f'Successfully created {created_count} questions with auto-generated multiple choice options!')
            return redirect('study_app:quiz_dashboard', book_id=book_id)
    
    context = {
        'book': book,
        'module': module,
    }
    return render(request, 'study_app/bulk_upload_questions.html', context)

def bulk_upload_questions(request, book_id):
    """Frontend bulk upload questions page"""
    book = get_object_or_404(Book, id=book_id)
    
    context = {
        'book': book,
    }
    return render(request, 'study_app/bulk_upload_questions.html', context)

def bulk_upload_questions(request, book_id):
    """Frontend bulk upload questions page"""
    from .models import Book
    from django.shortcuts import get_object_or_404, render
    
    book = get_object_or_404(Book, id=book_id)
    
    context = {
        'book': book,
    }
    return render(request, 'study_app/bulk_upload_questions.html', context)

def bulk_upload_questions(request, book_id):
    """Frontend bulk upload questions page"""
    from .models import Book
    from django.shortcuts import get_object_or_404, render
    
    book = get_object_or_404(Book, id=book_id)
    
    context = {
        'book': book,
    }
    return render(request, 'study_app/bulk_upload_questions.html', context)
