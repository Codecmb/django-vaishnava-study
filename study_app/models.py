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