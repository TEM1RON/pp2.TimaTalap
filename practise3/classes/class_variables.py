class Student:
    university = "KBTU"

    def __init__(self, name):
        self.name = name


student1 = Student("Temirlan")
student2 = Student("Alex")

print(student1.name)
print(student2.name)

print(student1.university)
print(student2.university)