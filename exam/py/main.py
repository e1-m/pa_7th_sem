class BuildingType:
    def __init__(self, name, texture, color):
        self.name = name
        self.texture = texture
        self.color = color


class BuildingFactory:
    def __init__(self):
        self.types = {}

    def get_building_type(self, name, texture, color):
        key = f"{name}|{texture}|{color}"
        if key not in self.types:
            self.types[key] = BuildingType(name, texture, color)
        return self.types[key]


class Building:
    def __init__(self, x, y, building_type):
        self.x = x
        self.y = y
        self.type = building_type

    def display(self):
        print(
            f"Displaying {self.type.name} at ({self.x},{self.y}) with {self.type.texture} texture "
            f"and {self.type.color} color\n memory address of the type: {id(self.type)}\n"
        )


def main():
    factory = BuildingFactory()

    b1 = Building(10, 20, factory.get_building_type("House", "Brick", "Red"))
    b2 = Building(15, 25, factory.get_building_type("House", "Brick", "Red"))
    b3 = Building(5, 10, factory.get_building_type("Shop", "Wood", "Blue"))

    b1.display()
    b2.display()
    b3.display()


if __name__ == "__main__":
    main()
