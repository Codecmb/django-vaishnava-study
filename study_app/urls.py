from django.urls import path
from . import views
from . import views_quiz

app_name = 'study_app'

urlpatterns = [
    # Existing URLs
    path('', views.index, name='index'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/qa/', views.qa_section, name='qa_section'),
    path('upload/qa/', views.upload_qa, name='upload_qa'),
    path('upload/study-material/', views.upload_study_material, name='upload_study_material'),
    path('delete-material/<int:material_id>/', views.delete_study_material, name='delete_study_material'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('test/static/', views.test_static, name='test_static'),
    
    # Quiz URLs
    path('book/<int:book_id>/quiz/', views_quiz.quiz_dashboard, name='quiz_dashboard'),
    path('book/<int:book_id>/quiz/module/<int:module_id>/', views_quiz.take_quiz, name='take_quiz'),
    path('quiz/results/<int:attempt_id>/', views_quiz.quiz_results, name='quiz_results'),
    path('book/<int:book_id>/quiz/add-question/', views_quiz.add_quiz_question, name='add_quiz_question'),
    path('course/<int:course_id>/add-quiz-module/', views_quiz.add_quiz_module, name='add_quiz_module'),
    
    # Profile redirect
    path('accounts/profile/', views.profile_redirect, name='profile_redirect'),
]
