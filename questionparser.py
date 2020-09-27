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


import json
from enum import Enum, auto
import re
questions = []
page_index = 0
part = ''
answer_index = 0
question_index = 0
correct_answer = ''
prompt = ''
question = {}
question_count = 0
answer_text = ''


class ReadingState(Enum):
    ITEM_START_PART = auto()
    ITEM_CAPTURE_PART_NAME = auto()
    ITEM_CAPTURE_INSTRUCTION_LINE = auto()
    ITEM_CAPTURE_PROMPT_FIRST_LINE = auto()
    ITEM_CAPTURE_PROMPT = auto()
    ITEM_CAPTURE_ANSWER = auto()
    RATIONALE_START_PART = auto()
    RATIONALE_CAPTURE_PART_NAME = auto()
    RATIONALE_CAPTURE_QUESTION_INDEX = auto()
    RATIONALE_CAPTURE_CORRECT_ANSWER = auto()
    RATIONALE_CAPTURE_RATIONALE = auto()


reading_state = ReadingState.ITEM_START_PART


class Question():
    def __init__(self):
        self.part = ''
        self.answers = []
        self.index = None
        self.prompt = ''
        self.correct_answer = ''
        self.rationale = ''


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


def maybe_item_prompt_first_line(text):
    pattern = re.compile(r'^(\d+)\. (.+)')
    m = pattern.search(text)
    if m:
        return True
    else:
        return False


def get_item_question_index_from_line(text):
    pattern = re.compile(r'^(\d+)\.')
    m = pattern.search(text)
    if m:
        return m.group(1)
    else:
        return None


def get_item_prompt_first_line_from_line(text):
    pattern = re.compile(r'^(\d+)\. (.+)')
    m = pattern.search(text)
    if m:
        return m.group(2)
    else:
        return None


def is_new_answer_line(text):
    pattern = re.compile(r'^[A-Z]\. (.+)')
    m = pattern.search(text)
    if m:
        return True
    else:
        return False


def handle_item_states(reading_state):
    if reading_state == ReadingState.ITEM_START_PART:
        reading_state = ReadingState.ITEM_CAPTURE_PART_NAME
    elif reading_state == ReadingState.ITEM_CAPTURE_PART_NAME:
        reading_state = ReadingState.ITEM_CAPTURE_INSTRUCTION_LINE
    elif reading_state == ReadingState.ITEM_CAPTURE_INSTRUCTION_LINE:
        reading_state = ReadingState.ITEM_CAPTURE_PROMPT_FIRST_LINE
    elif reading_state == ReadingState.ITEM_CAPTURE_PROMPT_FIRST_LINE:
        reading_state = ReadingState.ITEM_CAPTURE_PROMPT

    return reading_state


def handle_rationale_states(reading_state):
    if reading_state == ReadingState.RATIONALE_START_PART:
        reading_state = ReadingState.RATIONALE_CAPTURE_PART_NAME
    elif reading_state == ReadingState.RATIONALE_CAPTURE_PART_NAME:
        reading_state = ReadingState.RATIONALE_CAPTURE_QUESTION_INDEX
    elif reading_state == ReadingState.RATIONALE_CAPTURE_QUESTION_INDEX:
        reading_state = ReadingState.RATIONALE_CAPTURE_CORRECT_ANSWER
    elif reading_state == ReadingState.RATIONALE_CAPTURE_CORRECT_ANSWER:
        reading_state = ReadingState.RATIONALE_CAPTURE_RATIONALE
    return reading_state


def find_question_index_by_number_and_part(questions, index, part):
    return next((i for (i, item) in enumerate(questions) if (item.index == index and item.part == part)), None)


# open text file
with open('modified.txt', 'r') as questionTextFile:

    # start reading lines
    for line in questionTextFile:
        sanitizedLine = str.rstrip(line)

        # Item states
        reading_state = handle_item_states(reading_state)

        # Rationale States
        reading_state = handle_rationale_states(reading_state)

        # Identify Item section
        if is_item_section_start_line(sanitizedLine):
            reading_state = ReadingState.ITEM_START_PART
            part = questionTextFile.readline().rstrip()
            # print(part)
            # Next line is the part name to store
        elif is_rationale_section_start_line(sanitizedLine):
            # close last question
            question.answers.append(answer_text.strip())
            questions.append(question)
            # print(len(questions))
            reading_state = ReadingState.RATIONALE_CAPTURE_PART_NAME
            part = questionTextFile.readline().rstrip()
            continue
            # print(part)
        elif is_rationale_question_index_line(sanitizedLine):
            question_number = get_rationale_question_index_from_line(
                sanitizedLine)
            # lookup question by index and part
            question_index = find_question_index_by_number_and_part(
                questions, question_number, part)
            reading_state = ReadingState.RATIONALE_CAPTURE_QUESTION_INDEX
            continue
            # print(' '.join((part, get_rationale_question_index_from_line(sanitizedLine))))
        elif is_correct_answer_line(sanitizedLine):
            questions[question_index].correct_answer = get_correct_answer_from_line(
                sanitizedLine)
            reading_state = ReadingState.RATIONALE_CAPTURE_CORRECT_ANSWER
            continue
            # print(' '.join((part, get_correct_answer_from_line(sanitizedLine))))
        elif is_instruction_line(sanitizedLine):
            reading_state = ReadingState.ITEM_CAPTURE_INSTRUCTION_LINE
            continue

            # Identify item answers
        if reading_state == ReadingState.ITEM_CAPTURE_ANSWER:
            # Special case for the first answer
            if len(question.answers) == 0 and len(answer_text) == 0:
                answer_text = sanitizedLine[2:]
                continue
            # Append to the answer unless we get a new answer
            elif is_new_answer_line(sanitizedLine):
                question.answers.append(answer_text.strip())
                # answer_index += 1
                answer_text = sanitizedLine[2:]
            else:
                # peek at next line to see if it's a question
                if (maybe_item_prompt_first_line(sanitizedLine)):
                    question.answers.append(answer_text.strip())
                    questions.append(question)
                    reading_state = ReadingState.ITEM_CAPTURE_PROMPT_FIRST_LINE
                else:
                    answer_text = answer_text + ' ' + sanitizedLine
        # Instructions: For each question, select the most correct answer.

        # Read lines creating item prompt
        # Grab question index from first line
        if reading_state == ReadingState.ITEM_CAPTURE_PROMPT_FIRST_LINE:
            question = Question()
            question.part = part
            question.index = get_item_question_index_from_line(






                sanitizedLine)
            print(part + ' ' + question.index)
            question.prompt = get_item_prompt_first_line_from_line(






                sanitizedLine)
            # print(question['prompt'])
            # print(question)
            if sanitizedLine[-1] == '?':
                reading_state = ReadingState.ITEM_CAPTURE_ANSWER
                answer_text = ''
                answer_index = 0
            continue

        if reading_state == ReadingState.ITEM_CAPTURE_PROMPT:
            # Append to the prompt until we get to the question mark
            question.prompt += ' ' + sanitizedLine
            # print(question['prompt'])
            if sanitizedLine[-1] == '?':
                reading_state = ReadingState.ITEM_CAPTURE_ANSWER
                answer_text = ''
                answer_index = 0
                continue

        # Identify Rational Section
        # Part x Answers:
        # Part Name

        # Get item number X. Rationale
        # Get correct answer letter
        # Get answer explanation

        if reading_state == ReadingState.RATIONALE_CAPTURE_RATIONALE:
            # add to rationale
            questions[question_index].rationale = questions[question_index].rationale + \
                ' ' + sanitizedLine

questionTextFile.closed

print(str(page_index)+' Pages')
print(str(len(questions))+' Questions')

with open('questions.json', 'w') as outfile:
    json.dump([q.__dict__ for q in questions], outfile)
