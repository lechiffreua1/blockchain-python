import json


class Vehicle:
    def __init__(self, top_speed=100):
        self.top_speed = top_speed
        self.__warnings = []

    def __repr__(self):
        return 'Speed - {speed}, Warnings - {warn}'.format(speed=self.top_speed, warn=self.__warnings)

    def __str__(self):
        return 'String for Car instance'

    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings

    def print_top_speed(self):
        print('Top speed is {}'.format(self.top_speed))

    def print_warnings(self):
        print('Warnings are {}'.format(json.dumps(self.__warnings)))

    def drive(self):
        print('I\'m driving')

