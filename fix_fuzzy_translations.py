import polib

def fix_fuzzy_translations():
    po_file_path = 'locale/es/LC_MESSAGES/django.po'
    
    print(f"Opening PO file: {po_file_path}")
    po = polib.pofile(po_file_path)
    
    # Find and fix the problematic entries
    entries_to_fix = [
        ('Back to Courses', 'Volver a los Cursos'),
        ('Study This Book', 'Estudiar Este Libro')
    ]
    
    for msgid, correct_translation in entries_to_fix:
        entry = po.find(msgid)
        if entry:
            print(f"Fixing: {msgid}")
            print(f"  Current flags: {entry.flags}")
            print(f"  Current translation: '{entry.msgstr}'")
            
            # Remove fuzzy flag
            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')
                print("  ✅ Removed 'fuzzy' flag")
            
            # Update translation
            entry.msgstr = correct_translation
            print(f"  ✅ Updated to: '{correct_translation}'")
        else:
            print(f"❌ Entry not found: {msgid}")
    
    # Save the file
    po.save(po_file_path)
    print(f"\n✅ Fixed translations in {po_file_path}")

if __name__ == '__main__':
    fix_fuzzy_translations()
