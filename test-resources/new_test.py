class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed
    
    def speak(self):
        return f"{self.name} barks."

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color
    
    def speak(self):
        return f"{self.name} meows."

class AnimalShelter:
    def __init__(self):
        self.animals = []
    
    def add_animal(self, animal):
        self.animals.append(animal)
    
    def show_all(self):
        for animal in self.animals:
            print(f"{animal.name} is a {animal.species}.")
    
    def find_by_species(self, species):
        return [animal for animal in self.animals if animal.species == species]

def feed_animal(animal):
    return f"Feeding {animal.name}."

def main():
    shelter = AnimalShelter()
    dog = Dog("Rex", "German Shepherd")
    cat = Cat("Whiskers", "Gray")
    
    shelter.add_animal(dog)
    shelter.add_animal(cat)
    
    shelter.show_all()
    
    for animal in shelter.animals:
        print(animal.speak())
    
    print(feed_animal(dog))
    print(feed_animal(cat))
    
    dogs = shelter.find_by_species("Dog")
    for dog in dogs:
        print(f"{dog.name} is a dog.")
    
if __name__ == "__main__":
    main()
