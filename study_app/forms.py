from django import forms
from .models import QAUpload, Book, StudyMaterial

class QAUploadForm(forms.ModelForm):
    class Meta:
        model = QAUpload
        fields = ['book', 'csv_file', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.all().order_by('course__order', 'order')
        self.fields['csv_file'].help_text = 'Upload CSV file with columns: question_en,question_es,answer_en,answer_es,verse_reference,order'

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['book', 'title', 'material_type', 'language', 'description', 
                 'english_file', 'spanish_file', 'bilingual_file', 'verse_reference', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.all().order_by('course__order', 'order')
        self.fields['english_file'].help_text = 'Upload file for English version'
        self.fields['spanish_file'].help_text = 'Upload file for Spanish version'
        self.fields['bilingual_file'].help_text = 'Upload file containing both languages'
