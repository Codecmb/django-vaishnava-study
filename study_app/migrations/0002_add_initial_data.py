from django.db import migrations

def add_initial_data(apps, schema_editor):
    Course = apps.get_model('study_app', 'Course')
    Book = apps.get_model('study_app', 'Book')
    
    # Create courses
    bhakti_shastri = Course.objects.create(
        name="Bhakti Shastri",
        level="bhakti_shastri",
        description_en="Comprehensive study of the fundamental texts of Gaudiya Vaishnavism including Bhagavad-gita and essential scriptures.",
        description_es="Estudio completo de los textos fundamentales del Gaudiya Vaishnavismo incluyendo el Bhagavad-gita y las escrituras esenciales.",
        order=1
    )
    
    bhakti_vaibhava = Course.objects.create(
        name="Bhakti Vaibhava",
        level="bhakti_vaibhava",
        description_en="Advanced study of the first six cantos of Srimad Bhagavatam, exploring the spiritual dimensions of creation and devotion.",
        description_es="Estudio avanzado de los primeros seis cantos del Srimad Bhagavatam, explorando las dimensiones espirituales de la creación y la devoción.",
        order=2
    )
    
    bhakti_vedanta = Course.objects.create(
        name="Bhakti Vedanta",
        level="bhakti_vedanta",
        description_en="In-depth study of the later cantos of Srimad Bhagavatam, focusing on the pastimes of Lord Krishna and philosophical conclusions.",
        description_es="Estudio en profundidad de los cantos posteriores del Srimad Bhagavatam, centrándose en los pasatiempos del Señor Krishna y las conclusiones filosóficas.",
        order=3
    )
    
    bhakti_sarvabhauma = Course.objects.create(
        name="Bhakti Sarvabhauma",
        level="bhakti_sarvabhauma",
        description_en="The most advanced course covering the Caitanya Caritamrita and other advanced scriptures for serious spiritual practitioners.",
        description_es="El curso más avanzado que cubre el Caitanya Caritamrita y otras escrituras avanzadas para practicantes espirituales serios.",
        order=4
    )
    
    # Bhakti Shastri Books
    Book.objects.create(
        course=bhakti_shastri,
        title="Bhagavad-gita As It Is",
        english_url="https://vedabase.io/en/library/bg/",
        spanish_url="https://vedabase.io/es/library/bg/",
        order=1
    )
    
    Book.objects.create(
        course=bhakti_shastri,
        title="Sri Isopanishad",
        english_url="https://vedabase.io/en/library/iso/",
        spanish_url="https://vedabase.io/es/library/iso/",
        order=2
    )
    
    Book.objects.create(
        course=bhakti_shastri,
        title="Nectar of Devotion",
        english_url="https://vedabase.io/en/library/nod/",  # Fixed link
        spanish_url="https://vedabase.io/es/library/nod/",  # Fixed link
        order=3
    )
    
    Book.objects.create(
        course=bhakti_shastri,
        title="Nectar of Instruction",
        english_url="https://vedabase.io/en/library/noi/",  # Fixed link
        spanish_url="https://vedabase.io/es/library/noi/",  # Fixed link
        order=4
    )
    
    # Bhakti Vaibhava Books (Cantos 1-6)
    for i in range(1, 7):
        Book.objects.create(
            course=bhakti_vaibhava,
            title=f"Srimad Bhagavatam Canto {i}",
            english_url=f"https://vedabase.io/en/library/sb/{i}/",
            spanish_url=f"https://vedabase.io/es/library/sb/{i}/",
            order=i
        )
    
    # Bhakti Vedanta Books (Cantos 7-12)
    for i in range(7, 13):
        Book.objects.create(
            course=bhakti_vedanta,
            title=f"Srimad Bhagavatam Canto {i}",
            english_url=f"https://vedabase.io/en/library/sb/{i}/",
            spanish_url=f"https://vedabase.io/es/library/sb/{i}/",
            order=i-6
        )
    
    # Bhakti Sarvabhauma Books
    sarvabhauma_books = [
        ("Caitanya Caritamrita", "https://vedabase.io/en/library/cc/", "https://vedabase.io/es/library/cc/", 1),
        ("Teachings of Lord Caitanya", "https://vedabase.io/en/library/tlc/", "https://vedabase.io/es/library/tlc/", 2),
        ("Sri Caitanya Mahaprabhu - His Life and Precepts", "https://vedabase.io/en/library/cmpp/", "https://vedabase.io/es/library/cmpp/", 3),
        ("The Science of Self Realization", "https://vedabase.io/en/library/sr/", "https://vedabase.io/es/library/sr/", 4),
    ]
    
    for title, eng_url, esp_url, order in sarvabhauma_books:
        Book.objects.create(
            course=bhakti_sarvabhauma,
            title=title,
            english_url=eng_url,
            spanish_url=esp_url,
            order=order
        )

def remove_initial_data(apps, schema_editor):
    Course = apps.get_model('study_app', 'Course')
    Course.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('study_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
