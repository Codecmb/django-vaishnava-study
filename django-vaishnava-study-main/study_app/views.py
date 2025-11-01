from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import get_language, activate, gettext as _
from django.contrib import messages
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
def enhance_quiz_dashboard():
    """Helper function to enhance quiz dashboard data"""
    pass

@login_required
def take_quiz_professional(request, book_id, module_id):
    """Professional quiz interface with pagination and multiple choice"""
    from django.core.paginator import Paginator
    import json
    
    book = get_object_or_404(Book, id=book_id)
    module = get_object_or_404(QuizModule, id=module_id)
    questions = module.questions.all().order_by('order')
    
    # Prepare questions with multiple choice options
    for question in questions:
        if question.multiple_choice_options:
            try:
                question.multiple_choice_options_list = json.loads(question.multiple_choice_options)
            except:
                # If no multiple choice options, generate some
                question.multiple_choice_options_list = [
                    "The eternal nature of spiritual reality",
                    "A temporary material manifestation", 
                    "A product of the material energy",
                    "A form of illusion (maya)"
                ]
        else:
            question.multiple_choice_options_list = [
                "The eternal nature of spiritual reality",
                "A temporary material manifestation",
                "A product of the material energy", 
                "A form of illusion (maya)"
            ]
    
    # Pagination - 5 questions per page
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'book': book,
        'module': module,
        'page_questions': page_obj,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else 1,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else paginator.num_pages,
        'progress_percentage': int((page_obj.number - 1) / paginator.num_pages * 100),
        'start_index': (page_obj.number - 1) * 5 + 1,
    }
    
    return render(request, 'study_app/take_quiz_professional.html', context)

@login_required
def bulk_questions(request):
    """Bulk question entry form"""
    from .models import QuizModule, Book, QuizQuestion
    import json
    
    modules = QuizModule.objects.all().order_by('course__name', 'name')
    
    if request.method == 'POST':
        try:
            questions_text = request.POST.get('questions_text', '')
            module_id = request.POST.get('module_id')
            chapter = request.POST.get('chapter', '')
            
            module = QuizModule.objects.get(id=module_id)
            book = Book.objects.filter(course=module.course).first()
            
            # Parse questions (one per line, format: Question|Verse|Correct Answer|Hint)
            lines = [line.strip() for line in questions_text.split('\n') if line.strip()]
            imported = 0
            
            for i, line in enumerate(lines):
                parts = line.split('|')
                if len(parts) >= 3:
                    question_text = parts[0].strip()
                    verse = parts[1].strip() if len(parts) > 1 else ''
                    correct_answer = parts[2].strip() if len(parts) > 2 else ''
                    hint = parts[3].strip() if len(parts) > 3 else ''
                    
                    # Generate multiple choice options
                    options = generate_options_based_on_question(question_text, correct_answer)
                    
                    QuizQuestion.objects.create(
                        book=book,
                        module=module,
                        chapter=chapter,
                        question_text=question_text,
                        correct_answers=correct_answer,
                        verse_reference=verse,
                        additional_guidance=hint,
                        multiple_choice_options=json.dumps(options),
                        order=(i + 1) * 10
                    )
                    imported += 1
            
            from django.contrib import messages
            messages.success(request, f'Successfully imported {imported} questions!')
            return redirect('bulk_question_entry')
            
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error importing questions: {e}')
    
    context = {
        'modules': modules,
        'total_questions': QuizQuestion.objects.count()
    }
    return render(request, 'study_app/bulk_question_entry.html', context)

def generate_options_based_on_question(question_text, correct_answer):
    """Generate multiple choice options based on question content"""
    question_lower = question_text.lower()
    
    if 'soul' in question_lower or 'eternal' in question_lower:
        return [
            correct_answer,
            "The soul is temporary and perishes with the body",
            "The soul is a product of material energy", 
            "The soul is an illusion created by the mind"
        ]
    elif 'bhakti' in question_lower or 'devotional' in question_lower:
        return [
            correct_answer,
            "A type of material meditation technique",
            "A method for economic development",
            "A form of mental speculation"
        ]
    elif 'karma' in question_lower:
        return [
            correct_answer,
            "A type of yoga for physical health",
            "The law of material attraction", 
            "A system of government"
        ]
    else:
        return [
            correct_answer,
            "A temporary material manifestation",
            "A product of the material energy",
            "A form of illusion (maya)"
        ]

@login_required
def bulk_questions(request):
    """Bulk question entry form"""
    from .models import QuizModule, Book, QuizQuestion
    import json
    
    modules = QuizModule.objects.all().order_by('course__name', 'name')
    
    if request.method == 'POST':
        try:
            questions_text = request.POST.get('questions_text', '')
            module_id = request.POST.get('module_id')
            chapter = request.POST.get('chapter', '')
            
            module = QuizModule.objects.get(id=module_id)
            book = Book.objects.filter(course=module.course).first()
            
            # Parse questions (one per line, format: Question|Verse|Correct Answer|Hint)
            lines = [line.strip() for line in questions_text.split('\n') if line.strip()]
            imported = 0
            
            for i, line in enumerate(lines):
                parts = line.split('|')
                if len(parts) >= 3:
                    question_text = parts[0].strip()
                    verse = parts[1].strip() if len(parts) > 1 else ''
                    correct_answer = parts[2].strip() if len(parts) > 2 else ''
                    hint = parts[3].strip() if len(parts) > 3 else ''
                    
                    # Generate multiple choice options
                    options = generate_options_based_on_question(question_text, correct_answer)
                    
                    QuizQuestion.objects.create(
                        book=book,
                        module=module,
                        chapter=chapter,
                        question_text=question_text,
                        correct_answers=correct_answer,
                        verse_reference=verse,
                        additional_guidance=hint,
                        multiple_choice_options=json.dumps(options),
                        order=(i + 1) * 10
                    )
                    imported += 1
            
            from django.contrib import messages
            messages.success(request, f'Successfully imported {imported} questions!')
            return redirect('bulk_question_entry')
            
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error importing questions: {e}')
    
    context = {
        'modules': modules,
        'total_questions': QuizQuestion.objects.count()
    }
    return render(request, 'study_app/bulk_question_entry.html', context)

def generate_options_based_on_question(question_text, correct_answer):
    """Generate multiple choice options based on question content"""
    question_lower = question_text.lower()
    
    if 'soul' in question_lower or 'eternal' in question_lower:
        return [
            correct_answer,
            "The soul is temporary and perishes with the body",
            "The soul is a product of material energy", 
            "The soul is an illusion created by the mind"
        ]
    elif 'bhakti' in question_lower or 'devotional' in question_lower:
        return [
            correct_answer,
            "A type of material meditation technique",
            "A method for economic development",
            "A form of mental speculation"
        ]
    elif 'karma' in question_lower:
        return [
            correct_answer,
            "A type of yoga for physical health",
            "The law of material attraction", 
            "A system of government"
        ]
    else:
        return [
            correct_answer,
            "A temporary material manifestation",
            "A product of the material energy",
            "A form of illusion (maya)"
        ]

@login_required
def process_bulk_questions(request, book_id):
    """Process bulk questions submission"""
    if request.method == 'POST':
        try:
            book = get_object_or_404(Book, id=book_id)
            module_id = request.POST.get('module')
            chapter = request.POST.get('chapter', '')
            questions_text = request.POST.get('questions_text', '')
            
            if not module_id:
                messages.error(request, 'Please select a module')
                return redirect('bulk_questions', book_id=book_id)
            
            module = QuizModule.objects.get(id=module_id)
            
            # Parse questions
            lines = [line.strip() for line in questions_text.split('\n') if line.strip()]
            imported_count = 0
            
            for i, line in enumerate(lines):
                if not line:
                    continue
                    
                # Support multiple formats
                if '|' in line:
                    parts = line.split('|')
                    question_text = parts[0].strip()
                    verse = parts[1].strip() if len(parts) > 1 else ''
                    correct_answer = parts[2].strip() if len(parts) > 2 else ''
                    hint = parts[3].strip() if len(parts) > 3 else 'Study the verse carefully'
                else:
                    question_text = line
                    verse = ''
                    correct_answer = ''
                    hint = 'Study the verse carefully'
                
                if question_text:
                    # Auto-generate professional multiple choice
                    options = generate_professional_options(question_text, correct_answer)
                    
                    # If no correct answer provided, use the first option
                    if not correct_answer:
                        correct_answer = options[0]
                    
                    QuizQuestion.objects.create(
                        book=book,
                        module=module,
                        chapter=chapter,
                        question_text=question_text,
                        correct_answers=correct_answer,
                        verse_reference=verse,
                        additional_guidance=hint,
                        multiple_choice_options=json.dumps(options),
                        order=(imported_count + 1) * 10
                    )
                    imported_count += 1
            
            messages.success(request, f'✅ Successfully added {imported_count} questions to {module.name}!')
            return redirect('study_app:quiz_dashboard', book_id=book_id)
            
        except Exception as e:
            messages.error(request, f'❌ Error adding questions: {str(e)}')
            return redirect('bulk_questions', book_id=book_id)
    
    return redirect('study_app:quiz_dashboard', book_id=book_id)
