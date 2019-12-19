from vehicle import Vehicle


class Bus(Vehicle):
    def __init__(self, top_speed=50):
        super().__init__(top_speed)
        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)

    def print_group(self):
        print('Passengers - {}'.format(self.passengers))


bus1 = Bus()
bus1.add_group(['Test', 'Super Test'])
bus1.print_group()
bus1.drive()