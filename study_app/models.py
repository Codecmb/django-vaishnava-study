from django.db import models
from django.utils.translation import gettext_lazy as _

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
    
    # File fields for different languages
    english_file = models.FileField(upload_to='study_materials/english/', blank=True, null=True)
    spanish_file = models.FileField(upload_to='study_materials/spanish/', blank=True, null=True)
    bilingual_file = models.FileField(upload_to='study_materials/bilingual/', blank=True, null=True)
    
    # For simple Q&A that don't need files
    questions_json = models.JSONField(blank=True, null=True)  # Store Q&A as JSON
    
    verse_reference = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
        return f"Upload for {self.book.title} - {self.uploaded_at}"
