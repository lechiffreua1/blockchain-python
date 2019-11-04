def outer_func(*args):
    print(args[0]())


outer_func(lambda: '\'{:^20}\''.format('INNER'))
