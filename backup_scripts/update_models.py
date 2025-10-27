#!/usr/bin/env python3
"""
Script to add AI validation fields to QuizQuestion model
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaishnava-study.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from study_app.models import QuizQuestion
from django.db import models

print("Current QuizQuestion model structure:")
for field in QuizQuestion._meta.fields:
    print(f"  {field.name}: {field.get_internal_type()}")

print("\nTo add AI fields, we need to:")
print("1. Modify models.py to add the new fields")
print("2. Create and run migrations")
