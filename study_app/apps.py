from django.apps import AppConfig

class StudyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'study_app'
    
    def ready(self):
        import study_app.signals
