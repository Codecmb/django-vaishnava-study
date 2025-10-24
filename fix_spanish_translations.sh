#!/bin/bash

set -e

echo "=== FOCUSED SPANISH TRANSLATION SETUP ==="
echo ""

# Create our project's locale directory if it doesn't exist
mkdir -p ./locale/es/LC_MESSAGES

echo "🔧 Setting up project-specific translations..."
echo ""

# Only extract messages from our app, not Django's built-in apps
echo "📝 Extracting translatable strings from our app only..."
python3 manage.py makemessages -l es -i "venv" --ignore="venv/*" --no-obsolete

echo ""
echo "🔨 Compiling only our project's translations..."
python3 manage.py compilemessages --ignore="venv"

echo ""
echo "📊 Our project's translation status:"
if [[ -f "./locale/es/LC_MESSAGES/django.po" ]]; then
    msgfmt --statistics "./locale/es/LC_MESSAGES/django.po" 2>&1
else
    echo "No PO file found at ./locale/es/LC_MESSAGES/django.po"
fi

echo ""
echo "🌐 Testing our Spanish URLs..."
cd /home/marlins/django-vaishnava-study && python3 -c "
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from django.urls import reverse
from django.utils.translation import activate

print('Available Spanish URLs:')
activate('es')
try:
    print('  Home:', reverse('study_app:index'))
    print('  Spanish Home:', '/es' + reverse('study_app:index'))
except Exception as e:
    print('  Error getting URLs:', e)
"

echo ""
echo "🧪 Testing actual translation in context..."
cd /home/marlins/django-vaishnava-study && python3 -c "
import os
import django
from django.test import RequestFactory
from django.utils.translation import activate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.views import index

# Test with actual request
factory = RequestFactory()

print('Testing translation context:')
print('English:')
activate('en')
request_en = factory.get('/')
request_en.LANGUAGE_CODE = 'en'
try:
    response_en = index(request_en)
    print('  Status:', response_en.status_code)
except Exception as e:
    print('  Error:', e)

print('Spanish:')
activate('es') 
request_es = factory.get('/es/')
request_es.LANGUAGE_CODE = 'es'
try:
    response_es = index(request_es)
    print('  Status:', response_es.status_code)
except Exception as e:
    print('  Error:', e)
"

echo ""
echo "✅ Focused Spanish translation setup completed!"
