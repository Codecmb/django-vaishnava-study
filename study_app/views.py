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
