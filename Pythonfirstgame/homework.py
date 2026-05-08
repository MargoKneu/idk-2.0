class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
    def print2(self):
        print(self.brand)
        print(self.model)
        print(self.year)

car1 = Car("MG",
           "ZS Hybrid",
           "2024")
car1.print2()