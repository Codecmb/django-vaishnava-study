import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaishnava_study.settings')
    django.setup()

from django.utils.translation import gettext as _
from django.utils.translation import activate

def test_all_translations():
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
    
    print("🧪 COMPREHENSIVE TRANSLATION TEST:")
    print("=" * 60)
    
    all_working = True
    for test_string in test_strings:
        translation = _(test_string)
        if translation != test_string:
            print(f"✅ WORKING: {test_string} -> {translation}")
        else:
            print(f"❌ STILL NOT WORKING: {test_string}")
            all_working = False
    
    print("=" * 60)
    if all_working:
        print("🎉 ALL TRANSLATIONS ARE WORKING!")
    else:
        print("⚠️  Some translations still need fixing")
    
    return all_working

if __name__ == '__main__':
    test_all_translations()
