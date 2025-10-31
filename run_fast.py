#!/usr/bin/env python
"""
Minimal startup wrapper to bypass slow Django initialization
"""
import os
import sys
import time

def main():
    start = time.time()
    
    # Minimal environment setup
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
    
    # Import Django core
    import django
    from django.conf import settings
    from django.core.management import execute_from_command_line
    
    django.setup()
    
    print(f"🚀 Django ready in {time.time() - start:.2f}s")
    
    # Execute the actual command
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
