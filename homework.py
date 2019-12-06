import json
import pickle

condition = True
JSON_FILE_PATH = './homework_file.txt'
PICKLE_FILE_PATH = './homework_file.p'


def get_user_choice():
    return input('Your choice: ')


user_data_list = []


while condition:
    print('1: add data')
    print('2: write data')
    print('3: for output')
    print('4: for exiting')

    user_choice = get_user_choice()

    if user_choice == '1':
        user_data_list.append(input('Enter data:\n'))

    elif user_choice == '2':
        with open(JSON_FILE_PATH, mode='w') as f:
            f.write(json.dumps(user_data_list))
            f.write('\n')

        with open(PICKLE_FILE_PATH, mode='wb') as f:
            f.write(pickle.dumps(user_data_list))

    elif user_choice == '3':
        with open(JSON_FILE_PATH, mode='r') as f:
            print('JSON: ', json.loads(f.read()))

        with open(PICKLE_FILE_PATH, mode='rb') as f:
            print('PICKLE: ', pickle.loads(f.read()))

    elif user_choice == '4':
        condition = False

    else:
        exit(1)
