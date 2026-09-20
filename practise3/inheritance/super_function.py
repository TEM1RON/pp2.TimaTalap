class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university


student = Student("Temirlan", "KBTU")

print(student.name)
print(student.university)
class Animal:
    def sound(self):
        print("Animal makes a sound")


class Dog(Animal):
    def sound(self):
        super().sound()
        print("Dog says: Woof!")


dog = Dog()

dog.sound()
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department


manager = Manager("Alex", 500000, "IT")

print(manager.name)
print(manager.salary)
print(manager.department)
