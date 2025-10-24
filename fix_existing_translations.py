import polib

def fix_translations():
    po_file_path = 'locale/es/LC_MESSAGES/django.po'
    
    print(f"Opening PO file: {po_file_path}")
    po = polib.pofile(po_file_path)
    
    # Corrections needed
    corrections = {
        'Back to Courses': 'Volver a los Cursos',
        'Study This Book': 'Estudiar Este Libro'
    }
    
    fixed_count = 0
    
    for msgid, correct_msgstr in corrections.items():
        entry = po.find(msgid)
        if entry:
            print(f"Found: '{msgid}'")
            print(f"  Current: '{entry.msgstr}'")
            print(f"  Correct: '{correct_msgstr}'")
            
            # Remove fuzzy flag if present
            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')
                print("  Removed 'fuzzy' flag")
            
            # Update translation
            entry.msgstr = correct_msgstr
            fixed_count += 1
            print(f"  ✅ Updated translation")
        else:
            print(f"❌ Not found: '{msgid}'")
    
    # Save the file
    po.save(po_file_path)
    print(f"\n✅ Fixed {fixed_count} translations in {po_file_path}")

if __name__ == '__main__':
    fix_translations()
