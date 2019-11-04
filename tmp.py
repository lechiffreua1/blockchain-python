test_list = [1, 2, 3]

test_tuple = (1, 2, 3)

test_dict = {
    'a': 1,
    'b': 2,
}

del(test_list[2])
del test_tuple
del(test_dict['a'])

print('List - {}'.format(test_list))
print('Dict - {}'.format(test_dict))
