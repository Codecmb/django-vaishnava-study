from django.contrib import admin
from .models import Course, Book, QuestionAnswer

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

class QAInline(admin.TabularInline):
    model = QuestionAnswer
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'order']
    list_filter = ['level']
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    inlines = [QAInline]

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['book', 'verse_reference', 'order']
    list_filter = ['book']