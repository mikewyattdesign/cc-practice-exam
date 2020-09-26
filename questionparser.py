"""
Question Parser
"""

"""
Desired output
List of items with 
- index
- part
- prompt
- answer_choices
- correct_answer
- rationale
"""

"""
Expected parts
--
Part 1 – Renal, Endocrine, and Metabolism Disorders in the ICU
Part 2 – Cardiovascular Critical Care
Part 3 – Pulmonary Critical Care
Part 4 – Critical Care Infectious Diseases
Part 5 – Gastrointestinal Disorders
Part 6 – Neurological Disorders
Part 7 – Hematologic and Oncologic Disorders
Part 8 – Surgery, Trauma, and Transplantation
Part 9 – Pharmacology and Toxicology
Part 10 – Research, Ethics, and Administration
"""
import re

questions = []
page_index = 0
part = ''
answer_index = 0
correct_answer = ''
prompt = ''

def is_item_section_start_line(text):
    section_start_pattern = re.compile(r'^Part \d+:$')
    m = section_start_pattern.match(text)
    if m:
        return True
    else:
        return False

def is_rationale_section_start_line(text):
    section_start_pattern = re.compile(r'^Part \d+ Answers:$')
    m = section_start_pattern.match(text)
    if m:
        return True
    else:
        return False


def get_rationale_question_index_from_line(text):
    pattern = re.compile(r'^(\d+)\. Rationale$')
    m = pattern.search(text)
    if m:
        return m.group(1)
    else:
        return False

def is_rationale_question_index_line(text):
    m = get_rationale_question_index_from_line(text)
    if m:
        return True
    else:
        return False

def get_correct_answer_from_line(text):
    pattern = re.compile(r'^Answer: ([A-Z])$')
    m = pattern.search(text)
    if m:
        return m.group(1)
    else:
        return False

def is_correct_answer_line(text):
    m = get_correct_answer_from_line(text)
    if m:
        return True
    else:
        return False

def is_instruction_line(text):
    return text == 'Instructions: For each question, select the most correct answer.'


# open text file
with open('modified.txt', 'r') as questionTextFile:

    # start reading lines
    for line in questionTextFile:
        sanitizedLine = str.rstrip(line)
        if len(sanitizedLine) == 0:
            page_index += 1
            continue
        # Identify Item section 
        if is_item_section_start_line(sanitizedLine):
            part = questionTextFile.readline().rstrip()
            print(part)
            # Next line is the part name to store
        elif is_rationale_section_start_line(sanitizedLine):
            part = questionTextFile.readline().rstrip()
            print(part)
        elif is_rationale_question_index_line(sanitizedLine):
            print(get_rationale_question_index_from_line(sanitizedLine))
        elif is_correct_answer_line(sanitizedLine):
            print(get_correct_answer_from_line(sanitizedLine))
        elif is_instruction_line(sanitizedLine):
            continue
        

        # Instructions: For each question, select the most correct answer.

        # Read lines creating item prompt

        # Identify item answers

        # Identify Rational Section
        # Part x Answers:
        # Part Name

        # Get item number X. Rationale
        # Get correct answer letter
        # Get answer explanation

questionTextFile.closed

print(str(page_index)+' Pages')
