class Student:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello, my name is {self.name}")


student1 = Student("Temirlan")

student1.say_hello()