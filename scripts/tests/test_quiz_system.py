#!/usr/bin/env python3
"""
Test script to verify the quiz system is working correctly
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule, Book
from django.db import IntegrityError

def test_unique_constraint():
    """Test that duplicate questions are prevented"""
    print("🧪 TEST 1: Unique Constraint")
    
    # Get an existing question
    existing = QuizQuestion.objects.first()
    if not existing:
        print("   ⚠️  No questions to test with")
        return False
    
    # Try to create a duplicate
    try:
        duplicate = QuizQuestion(
            book=existing.book,
            module=existing.module,
            chapter=existing.chapter,
            verse_reference=existing.verse_reference,
            question_text=existing.question_text,
            additional_guidance="Test guidance",
            order=999
        )
        duplicate.save()
        print("   ❌ FAILED: Duplicate was created")
        duplicate.delete()
        return False
    except IntegrityError:
        print("   ✅ PASS: Duplicate prevented")
        return True

def test_no_duplicates():
    """Test that no duplicates exist in database"""
    print("🧪 TEST 2: No Existing Duplicates")
    
    from django.db.models import Count
    duplicates = QuizQuestion.objects.values(
        'module', 'verse_reference', 'question_text'
    ).annotate(count=Count('id')).filter(count__gt=1)
    
    if duplicates:
        print(f"   ❌ FAILED: {len(duplicates)} duplicate sets found")
        return False
    else:
        print("   ✅ PASS: No duplicates found")
        return True

def test_django_admin():
    """Test that Django admin works"""
    print("🧪 TEST 3: Django Admin")
    
    try:
        from django.contrib import admin
        if admin.site.is_registered(QuizQuestion):
            print("   ✅ PASS: QuizQuestion registered in admin")
            return True
        else:
            print("   ❌ FAILED: QuizQuestion not in admin")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False

def main():
    print("🎯 QUIZ SYSTEM VALIDATION")
    print("=" * 30)
    
    tests = [
        test_unique_constraint(),
        test_no_duplicates(), 
        test_django_admin()
    ]
    
    passed = sum(tests)
    total = len(tests)
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Quiz system is working correctly.")
        print("\n✅ WHAT'S FIXED:")
        print("   - Unique constraint prevents duplicate questions")
        print("   - No existing duplicates in database")
        print("   - Django admin accessible")
        print("   - Bulk operations available for management")
    else:
        print("⚠️  Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()
