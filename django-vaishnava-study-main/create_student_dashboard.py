#!/usr/bin/env python3
import os
import django
import sys

sys.path.append('/home/marlins/Documents/GitHub/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizModule, QuizQuestion

def create_simple_student_view():
    """Create a basic student quiz interface"""
    
    print("🎯 CREATING STUDENT QUIZ INTERFACE")
    print("=" * 50)
    
    modules = QuizModule.objects.all()
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bhagavad-gita Quiz System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .module { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 8px; }
            .question { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #4CAF50; }
            .answer-box { margin: 10px 0; }
            textarea { width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>📖 Bhagavad-gita Quiz System</h1>
        
        <div class="module">
            <h2>Available Quiz Modules</h2>
    """
    
    for module in modules:
        questions_count = module.quizquestion_set.count()
        html_template += f"""
            <div style="background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3>{module.name}</h3>
                <p>{module.description}</p>
                <p><strong>{questions_count} questions available</strong></p>
                <button onclick="takeQuiz({module.id})">Take This Quiz</button>
            </div>
        """
    
    html_template += """
        </div>

        <div id="quiz-area" style="display: none;">
            <!-- Quiz questions will be loaded here -->
        </div>

        <script>
        function takeQuiz(moduleId) {
            // This would load the quiz questions via AJAX
            document.getElementById('quiz-area').style.display = 'block';
            document.getElementById('quiz-area').innerHTML = '<p>Loading quiz questions...</p>';
            
            // For now, just show a message
            document.getElementById('quiz-area').innerHTML = `
                <h2>Quiz Interface</h2>
                <p>This would show:</p>
                <ul>
                    <li>Multiple choice options (when added to model)</li>
                    <li>Written answer textarea</li>
                    <li>AI feedback area</li>
                    <li>Prabhupada commentary</li>
                </ul>
                <p><em>Multiple choice field needs to be added to QuizQuestion model first.</em></p>
            `;
        }
        </script>
    </body>
    </html>
    """
    
    # Save the template
    with open('student_quiz_template.html', 'w') as f:
        f.write(html_template)
    
    print("✅ Created student quiz template")
    print("📁 Saved as: student_quiz_template.html")
    print("\\n🎯 NEXT STEPS:")
    print("1. Add 'multiple_choice_options' field to QuizQuestion model")
    print("2. Create Django view to serve this template")
    print("3. Add the view to study_app/urls.py")
    print("4. Populate multiple choice options for existing questions")

if __name__ == "__main__":
    create_simple_student_view()

