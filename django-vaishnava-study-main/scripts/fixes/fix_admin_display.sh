#!/bin/bash
echo "🔧 FIXING ADMIN DISPLAY ISSUES"
echo "=============================="

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os

admin_file = 'study_app/admin.py'

# Read current admin content
with open(admin_file, 'r') as f:
    content = f.read()

print("📋 CURRENT ADMIN CONFIGURATION:")
print("Looking for QuizModuleAdmin and QuizQuestionAdmin configurations...")

# Show current configuration
import re

# Find QuizModuleAdmin config
module_match = re.search(r'class QuizModuleAdmin.*?}(?=\n\n|\nclass|\Z)', content, re.DOTALL)
if module_match:
    print("🔍 CURRENT QuizModuleAdmin:")
    print(module_match.group(0))
else:
    print("❌ QuizModuleAdmin not found")

# Find QuizQuestionAdmin config  
question_match = re.search(r'class QuizQuestionAdmin.*?}(?=\n\n|\nclass|\Z)', content, re.DOTALL)
if question_match:
    print("🔍 CURRENT QuizQuestionAdmin:")
    print(question_match.group(0))
else:
    print("❌ QuizQuestionAdmin not found")

# Now let's fix the issues
print("\n🔧 FIXING THE CONFIGURATION...")

# Fix 1: Update QuizModuleAdmin to show bulk actions
if 'class QuizModuleAdmin' in content:
    # Replace the entire QuizModuleAdmin class with corrected version
    new_quizmodule_admin = '''@admin.register(QuizModule)
class QuizModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'question_count', 'created_at']
    list_filter = ['book', 'created_at']
    search_fields = ['title', 'description']
    actions = ['duplicate_quiz', 'export_questions']
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = "Questions"
    
    def duplicate_quiz(self, request, queryset):
        """Duplicate selected quizzes"""
        for quiz in queryset:
            quiz.pk = None
            quiz.title += " (Copy)"
            quiz.save()
        self.message_user(request, f"Duplicated {queryset.count()} quizzes")
    duplicate_quiz.short_description = "Duplicate selected quizzes"
    
    def export_questions(self, request, queryset):
        """Export questions to CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quiz_questions.csv"'
        writer = csv.writer(response)
        writer.writerow(['Quiz', 'Chapter', 'Verse', 'Question'])
        for quiz in queryset:
            for question in quiz.questions.all():
                writer.writerow([quiz.title, question.chapter, question.verse_reference, question.question_text])
        return response
    export_questions.short_description = "Export questions to CSV"'''

    # Replace the old QuizModuleAdmin
    old_module_pattern = r'@admin\.register\(QuizModule\)\s*class QuizModuleAdmin.*?}(?=\n\n|\nclass|\Z)'
    content = re.sub(old_module_pattern, new_quizmodule_admin, content, flags=re.DOTALL)
    print("✅ Fixed QuizModuleAdmin")

# Fix 2: Update QuizQuestionAdmin to show bulk actions and delete
if 'class QuizQuestionAdmin' in content:
    # Replace the entire QuizQuestionAdmin class with corrected version
    new_quizquestion_admin = '''@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'verse_reference', 'module', 'chapter', 'order']
    list_filter = ['module', 'chapter', 'verse_reference']
    search_fields = ['question_text', 'verse_reference', 'chapter']
    list_per_page = 50
    actions = ['delete_duplicates', 'delete_selected']
    
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
    delete_duplicates.short_description = "Delete duplicate questions"'''

    # Replace the old QuizQuestionAdmin
    old_question_pattern = r'@admin\.register\(QuizQuestion\)\s*class QuizQuestionAdmin.*?}(?=\n\n|\nclass|\Z)'
    content = re.sub(old_question_pattern, new_quizquestion_admin, content, flags=re.DOTALL)
    print("✅ Fixed QuizQuestionAdmin")

# Write the updated content
with open(admin_file, 'w') as f:
    f.write(content)

print("🎉 Admin configuration fixed!")
print("🔄 Restart the Django server to see changes")
PYEOF

# Test the changes
echo ""
echo "🧪 TESTING FIXED ADMIN:"
python manage.py check
