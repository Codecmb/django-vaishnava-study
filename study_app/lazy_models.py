"""
Lazy model imports to speed up startup
"""
def get_quiz_question_model():
    from .models import QuizQuestion
    return QuizQuestion

def get_book_model():
    from .models import Book
    return Book

def get_quiz_module_model():
    from .models import QuizModule
    return QuizModule
