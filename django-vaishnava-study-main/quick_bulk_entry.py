#!/usr/bin/env python3
import os
import django
import sys
import json

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule, Book

def quick_bulk_entry():
    """Quick bulk entry without web interface"""
    
    print("🚀 QUICK BULK QUESTION ENTRY")
    print("=" * 50)
    
    # Sample questions for quick testing
    sample_questions = [
        "What is the eternal nature of the soul?|BG 2.13|The soul is eternal, indestructible, and cannot be killed|Soul cannot be burned, cut, wet, or dried",
        "How does the soul transmigrate?|BG 2.22|The soul changes bodies like changing clothes|Just as a person puts on new garments",
        "What is bhakti-yoga?|BG 14.26|The process of devotional service to Lord Krishna|The eternal function of the soul",
        "What is karma?|BG 4.17|Material activities that bind the soul to rebirth|Law of action and reaction",
        "Who is Krishna?|BG 10.8|The Supreme Personality of Godhead|Source of all incarnations"
    ]
    
    modules = QuizModule.objects.all().order_by('course__name', 'name')
    print("\nAvailable Modules:")
    for i, module in enumerate(modules, 1):
        print(f"{i}. {module.course.name}: {module.name}")
    
    try:
        choice = int(input("\nSelect module number: ")) - 1
        selected_module = modules[choice]
        book = Book.objects.filter(course=selected_module.course).first()
        
        print(f"\n📝 Adding sample questions to: {selected_module.name}")
        print("Using pre-defined sample questions...")
        
        imported = 0
        for i, question_line in enumerate(sample_questions, 1):
            parts = question_line.split('|')
            if len(parts) >= 3:
                question_text = parts[0].strip()
                verse = parts[1].strip()
                correct_answer = parts[2].strip()
                hint = parts[3].strip() if len(parts) > 3 else "Study the verse carefully"
                
                # Generate multiple choice options
                options = generate_options(question_text, correct_answer)
                
                # Create the question
                QuizQuestion.objects.create(
                    book=book,
                    module=selected_module,
                    chapter=selected_module.chapters_range,
                    question_text=question_text,
                    correct_answers=correct_answer,
                    verse_reference=verse,
                    additional_guidance=hint,
                    multiple_choice_options=json.dumps(options),
                    order=i * 10
                )
                imported += 1
                print(f"✅ Added: {question_text}")
        
        print(f"\n🎉 Successfully imported {imported} sample questions!")
        print(f"📊 {selected_module.name} now has {selected_module.questions.count()} questions")
        
    except (ValueError, IndexError):
        print("❌ Invalid selection")
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_options(question_text, correct_answer):
    """Generate multiple choice options"""
    question_lower = question_text.lower()
    
    if 'soul' in question_lower:
        return [
            correct_answer,
            "The soul is temporary and perishes with the body",
            "The soul is a product of material energy",
            "The soul is an illusion"
        ]
    elif 'bhakti' in question_lower:
        return [
            correct_answer,
            "A type of material meditation",
            "A method for economic development", 
            "A form of mental speculation"
        ]
    elif 'karma' in question_lower:
        return [
            correct_answer,
            "A type of yoga for health",
            "The law of material attraction",
            "A system of government"
        ]
    elif 'krishna' in question_lower:
        return [
            correct_answer,
            "A great historical philosopher",
            "A mythical character from stories", 
            "A symbol of nature"
        ]
    else:
        return [
            correct_answer,
            "A temporary material manifestation",
            "A product of material energy",
            "A form of illusion (maya)"
        ]

if __name__ == "__main__":
    quick_bulk_entry()
