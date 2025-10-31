import time
import os
import django

def test_stage(stage_name, test_func):
    start = time.time()
    try:
        result = test_func()
        elapsed = time.time() - start
        print(f'✓ {stage_name}: {elapsed:.3f}s')
        return result
    except Exception as e:
        elapsed = time.time() - start
        print(f'✗ {stage_name}: {elapsed:.3f}s - ERROR: {e}')
        return None

print("=== Startup Performance Test ===")

# Stage 1: Basic Django setup
def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
    django.setup()

test_stage("Django Setup", setup_django)

# Stage 2: Import models
def import_models():
    from study_app import models
    return models

test_stage("Import Models", import_models)

# Stage 3: Database connection
def test_db():
    from django.db import connection
    connection.ensure_connection()
    return connection

test_stage("Database Connection", test_db)

print("=== Test Complete ===")
