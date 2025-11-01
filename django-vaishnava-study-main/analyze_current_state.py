#!/usr/bin/env python3
import os

print("🔍 ANALYZING CURRENT QUIZ FUNCTIONALITY")
print("=" * 50)

# Check URLs
print("1. CURRENT QUIZ URLS:")
try:
    with open('study_app/urls.py', 'r') as f:
        content = f.read()
        quiz_urls = [line for line in content.split('\n') if 'quiz' in line.lower()]
        for url in quiz_urls:
            print(f"   {url.strip()}")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. CURRENT QUIZ VIEWS:")
try:
    with open('study_app/views.py', 'r') as f:
        content = f.read()
        if 'def quiz' in content:
            print("   Quiz views found in views.py")
        else:
            print("   No quiz views in main views.py")
except Exception as e:
    print(f"   Error: {e}")

# Check for separate quiz views file
if os.path.exists('study_app/views_quiz.py'):
    print("   views_quiz.py exists")
else:
    print("   views_quiz.py not found")

print("\n3. CURRENT TEMPLATES:")
templates_dir = 'study_app/templates/study_app'
if os.path.exists(templates_dir):
    quiz_templates = [f for f in os.listdir(templates_dir) if 'quiz' in f.lower()]
    for template in quiz_templates:
        print(f"   {template}")
else:
    print("   Templates directory not found")

print("\n4. MODEL STATUS:")
try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
    django.setup()
    
    from study_app.models import QuizQuestion, QuizModule
    questions_count = QuizQuestion.objects.count()
    modules_count = QuizModule.objects.count()
    
    print(f"   Quiz questions in database: {questions_count}")
    print(f"   Quiz modules in database: {modules_count}")
    
    if questions_count > 0:
        sample = QuizQuestion.objects.first()
        print(f"   Sample question: {sample.question_text[:50]}...")
        
except Exception as e:
    print(f"   Error checking models: {e}")

print("\n" + "=" * 50)
print("📊 ANALYSIS COMPLETE")
