from django.urls import path
from . import views

app_name = 'study_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/qa/', views.qa_section, name='qa_section'),
    path('upload-qa/', views.upload_qa, name='upload_qa'),
    path('upload-study-material/', views.upload_study_material, name='upload_study_material'),
    path('upload-success/', views.upload_success, name='upload_success'),
]
