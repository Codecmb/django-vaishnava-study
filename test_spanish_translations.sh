#!/bin/bash

set -e

echo "=== TESTING SPANISH TRANSLATIONS ==="
echo ""

# Check Django settings for internationalization
echo "🔧 Checking Django settings..."
python3 -c "
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from django.conf import settings

print('USE_I18N:', getattr(settings, 'USE_I18N', 'Not set'))
print('USE_L10N:', getattr(settings, 'USE_L10N', 'Not set'))
print('LANGUAGE_CODE:', getattr(settings, 'LANGUAGE_CODE', 'Not set'))
print('LANGUAGES:', getattr(settings, 'LANGUAGES', 'Not set'))
print('LOCALE_PATHS:', getattr(settings, 'LOCALE_PATHS', 'Not set'))

# Check middleware
middleware = getattr(settings, 'MIDDLEWARE', [])
i18n_middleware = any('LocaleMiddleware' in m for m in middleware)
print('LocaleMiddleware in MIDDLEWARE:', i18n_middleware)
"

echo ""
echo "📁 Checking locale directory structure..."
find ./locale -type f -name "*.po" -o -name "*.mo" 2>/dev/null | sort

echo ""
echo "🔄 Creating/updating Spanish PO files..."
python3 manage.py makemessages -l es -i "venv/*" --no-obsolete

echo ""
echo "🔨 Compiling translations..."
python3 manage.py compilemessages

echo ""
echo "📊 Translation statistics:"
for po_file in $(find ./locale -name "*.po"); do
    echo "→ $(basename $po_file)"
    msgfmt --statistics "$po_file" 2>&1 || echo "  No translations found"
done

echo ""
echo "🌐 Testing URL patterns..."
python3 -c "
from django.urls import get_resolver
from django.conf import settings

urlconf = settings.ROOT_URLCONF
resolver = get_resolver(urlconf)

# Check if i18n patterns are included
def check_i18n_urls(patterns, prefix=''):
    for pattern in patterns:
        if hasattr(pattern, 'pattern'):
            if 'i18n' in str(pattern.pattern):
                print(f'✓ Found i18n URL pattern: {prefix}{pattern.pattern}')
            if hasattr(pattern, 'url_patterns'):
                check_i18n_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        elif hasattr(pattern, 'url_patterns'):
            check_i18n_urls(pattern.url_patterns, prefix)

check_i18n_urls(resolver.url_patterns)
"

echo ""
echo "🧪 Testing translation in Python..."
python3 -c "
from django.utils.translation import gettext as _
from django.utils.translation import activate

# Test basic translation
print('Testing English:')
activate('en')
print('  Home ->', _('Home'))
print('  Courses ->', _('Courses'))
print('  Login ->', _('Login'))

print('Testing Spanish:')
activate('es')
print('  Home ->', _('Home'))
print('  Courses ->', _('Courses')) 
print('  Login ->', _('Login'))
"

echo ""
echo "✅ Spanish translation test completed!"
echo ""
echo "🚀 To test in browser:"
echo "   English: http://localhost:8000/"
echo "   Spanish: http://localhost:8000/es/"
echo ""
echo "📝 If translations don't show:"
echo "   1. Check that strings are wrapped in {% trans %} in templates"
echo "   2. Verify .mo files are compiled"
echo "   3. Ensure LocaleMiddleware is in MIDDLEWARE"
echo "   4. Restart the Django server after compiling messages"
