import logging

# Suppress PyPDF2 warnings
logging.getLogger('PyPDF2').setLevel(logging.ERROR)

# Add this to your settings.py or manage.py
print("PyPDF2 warnings suppressed")
