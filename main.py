import json
from settings import settings
from random import choice


# deletes a question/answer pair by id
def delete_card(data, id):
    result = data.pop(id, 0)
    if result:
        with open(settings['data_file'], 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print('The question has been deleted')
    else:
        print('Opps, something went wrong')


# presents a random piece of information from the DB to the user
def show_cards():
    with open(settings['data_file']) as file:
        data = json.load(file)
        ids = list(data.keys())
        while len(ids):
            id = choice(ids)
            print(f'Question: {data[id]["question"]}')
            answer = input('Your answer: ')
            if answer in settings['stop_words']:
                return
            elif answer in settings['delete_words']:
                file.close()
                delete_card(data, id)
                show_cards()
            print(f'Answer: {data[id]["answer"]}\n')
            ids.remove(id)
        print('You answered all questions!\n')


# adds questions to the DB
def add_cards():
    question = bytes(input('\nEnter a question: '), "utf-8").decode("unicode_escape")
    answer = bytes(input('\nEnter an answer: '), "utf-8").decode("unicode_escape")
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
