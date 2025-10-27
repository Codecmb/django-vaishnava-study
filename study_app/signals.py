from django.db.models.signals import post_save
from django.dispatch import receiver
from study_app.models import QuizQuestion
from .management.commands.generate_quiz_choices import Command as ChoiceGenerator

@receiver(post_save, sender=QuizQuestion)
def generate_choices_on_save(sender, instance, created, **kwargs):
    """Automatically generate multiple choice options when a question is created or updated"""
    if created or not instance.multiple_choice_options:
        generator = ChoiceGenerator()
        generator.generate_choices_for_question(instance)
