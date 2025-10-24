import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, '/home/marlins/django-vaishnava-study')

# Try different possible settings module names
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaishnava_study.settings')
    django.setup()
except:
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaishnava_study_app.settings')
        django.setup()
    except:
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_app.settings')
            django.setup()
        except Exception as e:
            print(f"Could not setup Django: {e}")
            sys.exit(1)

from django.utils.translation import gettext as _
from django.utils.translation import activate

activate('es')

test_strings = [
    'Back to Courses',
    'Study This Book', 
    'Read Online (English)',
    'Read Online (Spanish)',
    'Study Tools',
    'Study Questions',
    'Read Online',
    'Study Materials'
]

print("🧪 FINAL TRANSLATION TEST:")
print("=" * 50)

all_working = True
for test in test_strings:
    result = _(test)
    if result != test:
        print(f"✅ {test} -> {result}")
    else:
        print(f"❌ {test} -> {result}")
        all_working = False

print("=" * 50)
if all_working:
    print("🎉 ALL TRANSLATIONS ARE WORKING!")
else:
    print("⚠️ Some translations still need attention")
