persons = [
    {
        'name': 'Max',
        'age': 30,
        'hobbies': ['swimming', 'tv shows']
    },
    {
        'name': 'Bob',
        'age': 20,
        'hobbies': ['programming', 'eating']
    },
    {
        'name': 'john',
        'age': 40,
        'hobbies': ['eating', 'sleeping']
    }
]

print('Persons names: ', [person['name'] for person in persons])
print('Persons are older than 20 - ', all([person['age'] > 20 for person in persons]))

new_persons = [person.copy() for person in persons]
new_persons[0]['age'] = 32

print('Old first person - ', persons[0])
print('New first person - ', new_persons[0])

first_person, second_person, third_person = persons

print('First - ', first_person)
print('Second - ', second_person)
print('Third - ', third_person)
