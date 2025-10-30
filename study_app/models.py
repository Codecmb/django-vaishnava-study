from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Course(models.Model):
    COURSE_LEVELS = [
        ('bhakti_shastri', _('Bhakti Shastri')),
        ('bhakti_vaibhava', _('Bhakti Vaibhava')),
        ('bhakti_vedanta', _('Bhakti Vedanta')),
        ('bhakti_sarvabhauma', _('Bhakti Sarvabhauma')),
    ]
    
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=COURSE_LEVELS)
    description_en = models.TextField()
    description_es = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Book(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    english_url = models.URLField()
    spanish_url = models.URLField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class StudyMaterial(models.Model):
    MATERIAL_TYPES = [
        ('qa', _('Questions & Answers')),
        ('notes', _('Study Notes')),
        ('summary', _('Chapter Summary')),
        ('quiz', _('Quiz')),
        ('other', _('Other Material')),
    ]
    
    LANGUAGES = [
        ('en', _('English')),
        ('es', _('Spanish')),
        ('both', _('Both Languages')),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    language = models.CharField(max_length=10, choices=LANGUAGES)
    description = models.TextField(blank=True)
    
    english_file = models.FileField(upload_to='study_materials/english/', blank=True, null=True)
    spanish_file = models.FileField(upload_to='study_materials/spanish/', blank=True, null=True)
    bilingual_file = models.FileField(upload_to='study_materials/bilingual/', blank=True, null=True)
    questions_json = models.JSONField(blank=True, null=True)
    verse_reference = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ai_feedback = models.TextField(blank=True, null=True)
    ai_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_siddhanta_aligned = models.BooleanField(default=False)
    feedback_timestamp = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_material_type_display()}"

class QuestionAnswer(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='qas')
    question_en = models.TextField()
    question_es = models.TextField()
    answer_en = models.TextField()
    answer_es = models.TextField()
    verse_reference = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"QA for {self.book.title} – {self.verse_reference}"

class QAUpload(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='qa_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Upload for {self.book.title} – {self.uploaded_at}"

class QuizModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_modules')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    chapters_range = models.CharField(max_length=100, help_text="e.g., 'Chapters 1-6' or 'Chapters 7-12'")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"

class QuizQuestion(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quiz_questions')
    module = models.ForeignKey(QuizModule, on_delete=models.CASCADE, related_name='questions')
    chapter = models.CharField(max_length=10, help_text="e.g., 'Chapter 1' or 'Chapter 2'")
    question_text = models.TextField()
    correct_answers = models.TextField(blank=True, null=True)
    multiple_choice_options = models.TextField(blank=True, null=True)
    prabhupada_commentary = models.TextField(blank=True, null=True)
    additional_guidance = models.TextField(blank=True)
    verse_reference = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_choices_list(self):
        import json
        if self.multiple_choice_options:
            try:
                return json.loads(self.multiple_choice_options)
            except:
                return []
        return []

    def __str__(self):
        return f"{self.book.title} - {self.chapter}: {self.question_text[:50]}..."

    def check_answer(self, user_answer):
        import json
        if not user_answer or not self.correct_answers:
            return False
        
        if user_answer.isdigit():
            try:
                choices = json.loads(self.multiple_choice_options)
                selected_choice = choices[int(user_answer)]
                return selected_choice == self.correct_answers
            except:
                return False
        
        user_answer_clean = user_answer.strip().lower()
        correct_answers_clean = self.correct_answers.strip().lower()
        return user_answer_clean in correct_answers_clean or correct_answers_clean in user_answer_clean

    def get_correct_answers_list(self):
        """
        Return a list of correct answers for display in results.
        Handles both multiple choice and text answers.
        """
        import json
        if not self.correct_answers:
            return []
        
        # For multiple choice questions, return the correct choice text
        if self.multiple_choice_options:
            try:
                choices = json.loads(self.multiple_choice_options)
                # If correct_answers is an index, return the corresponding choice
                if self.correct_answers.isdigit():
                    index = int(self.correct_answers)
                    if 0 <= index < len(choices):
                        return [choices[index]]
                # If correct_answers matches a choice text, return it
                for choice in choices:
                    if choice.strip().lower() == self.correct_answers.strip().lower():
                        return [choice]
            except:
                pass
        
        # For text answers, return the correct answer as a list
        return [self.correct_answers.strip()]

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    module = models.ForeignKey(QuizModule, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Quiz Attempt - {self.book.title} - {self.module.name} - Score: {self.score}/{self.total_questions}"
    
    def calculate_score(self):
        score = 0
        for question_id, user_answer in self.answers.items():
            try:
                question = QuizQuestion.objects.get(id=question_id)
                if question.check_answer(user_answer):
                    score += 1
            except QuizQuestion.DoesNotExist:
                continue
        self.score = score
        self.total_questions = len(self.answers)
        self.save()
    
    def get_feedback(self):
        percentage = (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0
        if percentage >= 90:
            return "Excellent! Your understanding is very much in line with Srila Prabhupada's teachings. Hare Krishna!"
        elif percentage >= 70:
            return "Very good! You have a good grasp of the philosophy. Continue studying Srila Prabhupada's books."
        elif percentage >= 50:
            return "Good effort! There's always more to learn in Krishna consciousness. Keep reading and chanting."
        else:
            return "Thank you for your effort! Krishna consciousness is a gradual process. Keep studying Prabhupada's teachings."
    
    class Meta:
        ordering = ['-completed_at']

class BookPDF(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pdfs')
    pdf_file = models.FileField(upload_to='book_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text_extracted = models.BooleanField(default=False)
    extracted_text = models.TextField(blank=True)
    
    def __str__(self):
        return f"PDF for {self.book.title}"

# Add evaluation_results field to QuizAttempt if it doesn't exist
# If this causes issues, we'll create a proper migration

# Add this method to the QuizAttempt class if it doesn't exist
def calculate_score(self):
    """Calculate score using book-based evaluation"""
    from .book_based_evaluator import book_evaluator
    score = 0
    for question_id, user_answer in self.answers.items():
        try:
            question = QuizQuestion.objects.get(id=question_id)
            is_correct, feedback, commentary = book_evaluator.evaluate_answer(
                question=question.question_text,
                user_answer=user_answer
            )
            if is_correct:
                score += 1
        except QuizQuestion.DoesNotExist:
            continue
    
    self.score = score
    self.total_questions = len(self.answers)
    self.save()
    return score
