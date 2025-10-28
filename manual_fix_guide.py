print("=== MANUAL FIX GUIDE ===")
print("")
print("Open: nano ./study_app/models.py")
print("")
print("Find and fix these EXACT lines:")
print("")

with open('./study_app/models.py', 'r') as f:
    for i, line in enumerate(f, 1):
        if 'def __str__(self):\\n' in line:
            print(f"Line {i}: {line.strip()}")
            print("  FIX: Split into two lines:")
            print("       def __str__(self):")
            print("           return [the rest of the line]")
            print("")
