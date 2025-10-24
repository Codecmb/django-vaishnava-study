import polib

def add_missing():
    po_file_path = 'locale/es/LC_MESSAGES/django.po'
    
    print(f"Opening PO file: {po_file_path}")
    po = polib.pofile(po_file_path)
    
    # Missing translations to add
    missing_translations = {
        'Read Online (English)': 'Leer en Línea (Inglés)',
        'Read Online (Spanish)': 'Leer en Línea (Español)',
        'Study Tools': 'Herramientas de Estudio',
        'Study Questions': 'Preguntas de Estudio'
    }
    
    added_count = 0
    
    for msgid, msgstr in missing_translations.items():
        # Check if already exists
        if not po.find(msgid):
            print(f"Adding: '{msgid}' -> '{msgstr}'")
            entry = polib.POEntry(
                msgid=msgid,
                msgstr=msgstr,
                occurrences=[('./study_app/templates/study_app/', '1')]
            )
            po.append(entry)
            added_count += 1
        else:
            print(f"Already exists: '{msgid}'")
    
    # Save the file
    po.save(po_file_path)
    print(f"\n✅ Added {added_count} new translations to {po_file_path}")

if __name__ == '__main__':
    add_missing()
