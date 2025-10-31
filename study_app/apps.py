from django.apps import AppConfig

class StudyAppConfig(AppConfig):
    name = 'study_app'
    # No heavy ready() method to speed up startup
