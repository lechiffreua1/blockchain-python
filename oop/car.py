from vehicle import Vehicle


class Car(Vehicle):
    def brag(self):
        print('My Car can drive {} speed'.format(self.top_speed))


first_car = Car(200)
first_car.brag()
