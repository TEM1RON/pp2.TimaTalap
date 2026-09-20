class Animal:
    def sound(self):
        print("Some animal sound")


class Dog(Animal):
    def sound(self):
        print("Woof!")


class Cat(Animal):
    def sound(self):
        print("Meow!")


dog = Dog()
cat = Cat()

dog.sound()
cat.sound()
class Person:
    def introduce(self):
        print("I am a person")


class Student(Person):
    def introduce(self):
        super().introduce()
        print("I am a student")


student = Student()

student.introduce()
class Vehicle:
    def move(self):
        print("Vehicle is moving")


class Car(Vehicle):
    def move(self):
        print("Car is driving")


class Boat(Vehicle):
    def move(self):
        print("Boat is sailing")


car = Car()
boat = Boat()

car.move()
boat.move()
