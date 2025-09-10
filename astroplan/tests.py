from django.test import TestCase
import csv
# Create your tests here.


class Planet:
    def __init__(self, name, period, speed, color):
        self.name = name
        self.period = period
        self.speed = speed
        self.color = color

    def named(self):
        return f'The star name is {self.name}'

    def __str__(self):
        return f'{self.name}, {self.speed}, {self.period}, {self.color}'


p = Planet('Jupiter', 12, 2000000, 'blue')


class Stars(Planet):

    def __init__(self, name, speed, period, brightness):
        super().__init__(name, period, speed, color)
        self.brigthness = brightness


    def __str__(self):
        return f'{self.name}, {self.speed}, {self.period}'


s = Stars('Fireball', 2365, 32, 600, 'neon-purple')

print(s.named())