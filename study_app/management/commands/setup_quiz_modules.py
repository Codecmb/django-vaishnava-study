from django.core.management.base import BaseCommand
from study_app.models import Course, QuizModule

class Command(BaseCommand):
    help = 'Setup default quiz modules for all courses'
    
    def handle(self, *args, **options):
        # Define module structure for each course level
        course_modules = {
            'bhakti_shastri': [
                ('Module 1: Chapters 1-6', 'Chapters 1-6'),
                ('Module 2: Chapters 7-12', 'Chapters 7-12'), 
                ('Module 3: Chapters 13-18', 'Chapters 13-18'),
            ],
            'bhakti_vaibhava': [
                ('Module 1: First Half', 'First Half'),
                ('Module 2: Second Half', 'Second Half'),
            ],
            'bhakti_vedanta': [
                ('Module 1: First Third', 'First Third'),
                ('Module 2: Second Third', 'Second Third'),
                ('Module 3: Final Third', 'Final Third'),
            ],
            'bhakti_sarvabhauma': [
                ('Complete Course', 'All Chapters'),
            ]
        }
        
        for course in Course.objects.all():
            self.stdout.write(f"Setting up modules for {course.name} ({course.level})")
            
            if course.level in course_modules:
                modules = course_modules[course.level]
                for order, (name, chapters_range) in enumerate(modules, 1):
                    module, created = QuizModule.objects.get_or_create(
                        course=course,
                        name=name,
                        defaults={
                            'chapters_range': chapters_range,
                            'order': order
                        }
                    )
                    if created:
                        self.stdout.write(f"  Created: {name}")
                    else:
                        self.stdout.write(f"  Already exists: {name}")
        
        self.stdout.write(self.style.SUCCESS('Successfully setup all quiz modules'))
