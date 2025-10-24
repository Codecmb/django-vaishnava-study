import polib

def remove_duplicate_translations():
    po_file_path = 'locale/es/LC_MESSAGES/django.po'
    
    print(f"Opening PO file: {po_file_path}")
    po = polib.pofile(po_file_path)
    
    # Track seen message IDs and remove duplicates
    seen = set()
    unique_entries = []
    removed_count = 0
    
    for entry in po:
        if entry.msgid in seen:
            print(f"Removing duplicate: '{entry.msgid}'")
            removed_count += 1
        else:
            seen.add(entry.msgid)
            unique_entries.append(entry)
    
    # Replace the entries with unique ones
    po[:] = unique_entries
    
    # Save the file
    po.save(po_file_path)
    print(f"\n✅ Removed {removed_count} duplicate translations")
    print(f"✅ Total unique translations: {len(unique_entries)}")

if __name__ == '__main__':
    remove_duplicate_translations()
