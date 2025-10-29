#!/usr/bin/env python3
import subprocess
import os

print("🔗 QUICK GITHUB SETUP FOR Codecmb")
print("=" * 50)

# Check current setup
result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
print("📡 Remote Repository:")
print(result.stdout)

# Check what we're pushing
result = subprocess.run(['git', 'log', '--oneline', '-3'], capture_output=True, text=True)
print("📦 Commits to push:")
print(result.stdout)

print("\n🎯 SIMPLE PUSH INSTRUCTIONS:")
print("1. Get token from: https://github.com/settings/tokens")
print("2. Run: git push origin main")
print("3. When prompted:")
print("   Username: Codecmb")
print("   Password: [Your Token]")
print("")
print("💡 Or use direct method:")
print("   git push https://YOUR_TOKEN@github.com/Codecmb/django-vaishnava-study.git main")

print("\n🔗 Your repository will be at:")
print("   https://github.com/Codecmb/django-vaishnava-study")
