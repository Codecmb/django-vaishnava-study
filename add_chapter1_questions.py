from study_app.models import Book, QuizModule, QuizQuestion

# Get the book and module
book = Book.objects.get(title="Bhagavad-gita As It Is")
module = QuizModule.objects.get(course=book.course, name__contains="Module 1")

questions_data = [
    {
        'chapter': 'Chapter 1',
        'question_text': 'Why was Duryodhana confident of full support of Bhismadeva and Dronacarya in the battle? (1.11)',
        'correct_answers': 'they were obliged to fight for kauravas, bhisma and drona were appointed by dhritarashtra, they were bound by duty and relationship',
        'prabhupada_commentary': 'Duryodhana was confident of the support of Bhisma and Drona because they were obliged to maintain the royal order and fight for the Kauravas. Although they were not personally interested in the battle, they were bound by duty and their relationship with the royal family.',
        'verse_reference': 'Bg 1.11',
        'order': 1
    },
    {
        'chapter': 'Chapter 1',
        'question_text': 'List and explain the significance of the four signs of victory for the Pandavas. (BG 1.14-20)',
        'correct_answers': 'krishna blowing pancajanya, arjuna blowing devadatta, bhima blowing poundra, yudhisthira blowing anantavijaya, conchshells indicate divine support, auspicious beginning',
        'prabhupada_commentary': 'The blowing of the conchshells by Krishna and the Pandavas—Pancajanya by Krishna, Devadatta by Arjuna, Poundra by Bhima, and Anantavijaya by Yudhisthira—indicated their divine support and the auspicious beginning of their mission. The conchshells symbolized their transcendental position and the certainty of their victory.',
        'verse_reference': 'Bg 1.14-20',
        'order': 2
    },
    {
        'chapter': 'Chapter 1',
        'question_text': 'What is the meaning of the word gudakesa? (1.24)',
        'correct_answers': 'conqueror of sleep, conqueror of ignorance, one who has conquered sleep',
        'prabhupada_commentary': 'The word "Gudakesa" refers to one who has conquered sleep or ignorance. It indicates that Arjuna could overcome the darkness of ignorance, which made him qualified to receive the transcendental knowledge of the Bhagavad-gita.',
        'verse_reference': 'Bg 1.24',
        'order': 3
    },
    {
        'chapter': 'Chapter 1', 
        'question_text': 'List the six kinds of aggressors. (1.36)',
        'correct_answers': 'gurus, grandfathers, teachers, maternal uncles, grandsons, fathers-in-law, friends',
        'prabhupada_commentary': 'Arjuna mentions six kinds of aggressors: gurus (teachers), grandfathers, teachers, maternal uncles, grandsons, fathers-in-law, and other relatives and friends. He was reluctant to fight against these respected persons.',
        'verse_reference': 'Bg 1.36',
        'order': 4
    },
    {
        'chapter': 'Chapter 1',
        'question_text': 'List the various consequences due to the destruction of the dynasty. (1.39-42)',
        'correct_answers': 'destruction of family traditions, increase of unwanted population, degradation of family duties, mixing of castes, hellish life for ancestors, disruption of social and spiritual order',
        'prabhupada_commentary': 'The consequences of dynasty destruction include: 1) Destruction of family traditions and religious principles, 2) Increase of unwanted population (varna-sankara), 3) Degradation of family duties, 4) Mixing of castes leading to social chaos, 5) Hellish life for ancestors who are deprived of offerings, 6) Disruption of the entire social and spiritual order.',
        'verse_reference': 'Bg 1.39-42',
        'order': 5
    },
    {
        'chapter': 'Chapter 1',
        'question_text': 'Which quality of Arjuna makes him fit to receive the knowledge of Bhagavad-Gita, according to the last purport of Chapter 1?',
        'correct_answers': 'surrender to krishna, acceptance of krishna as spiritual master, submissive inquiry, humility',
        'prabhupada_commentary': 'In the last purport of Chapter 1, Srila Prabhupada explains that Arjuna\'s qualification to receive the knowledge of Bhagavad-gita was his complete surrender to Krishna as his spiritual master. Arjuna set aside his so-called knowledge and submitted to Krishna as a disciple, saying "I am Your disciple, and a soul surrendered unto You. Please instruct me." This submissive attitude made him eligible for transcendental knowledge.',
        'verse_reference': 'Bg 1.46 Purport',
        'order': 6
    }
]

for i, q_data in enumerate(questions_data, 1):
    QuizQuestion.objects.create(
        book=book,
        module=module,
        chapter=q_data['chapter'],
        question_text=q_data['question_text'],
        correct_answers=q_data['correct_answers'],
        prabhupada_commentary=q_data['prabhupada_commentary'],
        verse_reference=q_data['verse_reference'],
        order=q_data['order']
    )
    print(f"Added Chapter 1 question {i}: {q_data['question_text'][:50]}...")

print(f"Successfully added {len(questions_data)} Chapter 1 questions!")
