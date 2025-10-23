from django import forms
from .models import QAUpload, StudyMaterial, QuizQuestion, QuizModule

class QAUploadForm(forms.ModelForm):
    class Meta:
        model = QAUpload
        fields = ['book', 'csv_file', 'notes']

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['book', 'title', 'material_type', 'language', 'description', 
                 'english_file', 'spanish_file', 'bilingual_file', 'verse_reference', 'order']

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['book', 'module', 'chapter', 'question_text', 'correct_answers', 
                 'prabhupada_commentary', 'additional_guidance', 'verse_reference', 'order']
        widgets = {
            'correct_answers': forms.TextInput(attrs={
                'placeholder': 'Enter comma-separated acceptable answers'
            }),
            'prabhupada_commentary': forms.Textarea(attrs={'rows': 4}),
            'additional_guidance': forms.Textarea(attrs={'rows': 3}),
        }

class QuizModuleForm(forms.ModelForm):
    class Meta:
        model = QuizModule
        fields = ['course', 'name', 'description', 'chapters_range', 'order']

class QuizAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.question_text,
                widget=forms.Textarea(attrs={
                    'rows': 4,
                    'placeholder': 'Share your understanding based on Srila Prabhupada\'s teachings...',
                    'class': 'form-control quiz-answer'
                }),
                required=False,
                help_text=f"Verse: {question.verse_reference}" if question.verse_reference else ""
            )
