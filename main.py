import json
from settings import settings
from random import choice


# presents a random piece of information from the DB to the user
def show_cards():
    with open(settings['data_file']) as file:
        data = json.load(file)
        ids = list(data.keys())
        while len(ids):
            id = choice(ids)
            print(f'Question: {data[id]["question"]}')
            if input('Your answer: ') in settings['stop_words']:
                return
            print(f'Answer: {data[id]["answer"]}\n')
            ids.remove(id)
        print('You answered all questions!\n')


# adds questions to the DB
def add_cards():
    question = input('\nEnter a question: ')
    answer = input('\nEnter an answer: ')
    if question in settings['stop_words'] or answer in settings['stop_words']:
        return
    with open(settings['data_file']) as file:
        data = json.load(file)
    data[len(data) + 1] = {
        "question": question,
        "answer": answer
    }
    with open(settings['data_file'], 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


while True:
    command = input(settings['menu_text'])
    if command == 'learn':
        show_cards()
    elif command == 'add':
        add_cards()
    elif command in settings['stop_words']:
        break
