from django.urls import path
from . import views

app_name = 'vaishnava_study'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/qa/', views.qa_section, name='qa_section'),
]