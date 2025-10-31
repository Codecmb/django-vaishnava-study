#!/usr/bin/env python
import os
import sys
import time

def main():
    start_total = time.time()
    
    # Minimal Django setup
    start = time.time()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
    import django
    django.setup()
    print(f"Django setup: {time.time()-start:.3f}s")
    
    # Quick test
    start = time.time()
    from study_app.models import QuizQuestion
    count = QuizQuestion.objects.count()
    print(f"Database query: {time.time()-start:.3f}s")
    print(f"Total questions: {count}")
    
    print(f"TOTAL TIME: {time.time()-start_total:.3f}s")

if __name__ == '__main__':
    main()
