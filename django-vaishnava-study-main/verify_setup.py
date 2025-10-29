#!/usr/bin/env python3
import os
import subprocess
import sys

print("🔧 Verifying Django Setup")
print("=" * 40)

# Check manage.py
if not os.path.exists('manage.py'):
    print("❌ manage.py not found - creating it...")
    with open('manage.py', 'w') as f:
        f.write('''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
''')
    print("✅ manage.py created")
else:
    print("✅ manage.py exists")

# Make executable
os.chmod('manage.py', 0o755)

# Test Django
commands = [
    ['python3', 'manage.py', '--version'],
    ['python3', 'manage.py', 'check'],
]

for cmd in commands:
    try:
        print(f"\n🚀 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ SUCCESS: {result.stdout.strip()}")
        else:
            print(f"❌ FAILED: {result.stderr}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

print(f"\n🎉 Setup verification complete!")

