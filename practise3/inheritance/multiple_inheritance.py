class Father:
    def drive(self):
        print("Father can drive")


class Mother:
    def cook(self):
        print("Mother can cook")


class Child(Father, Mother):
    pass


child = Child()

child.drive()
child.cook()
class Programmer:
    def code(self):
        print("Writing code")


class Designer:
    def design(self):
        print("Creating design")


class WebDeveloper(Programmer, Designer):
    pass


developer = WebDeveloper()

developer.code()
developer.design()
class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        super().show()
        print("B")


class C(A):
    def show(self):
        super().show()
        print("C")


class D(B, C):
    def show(self):
        super().show()
        print("D")


obj = D()

obj.show()
