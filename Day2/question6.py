from abc import ABC,abstractmethod
class Bird(ABC):
    @abstractmethod
    def move():
        pass

class SwimmingBird(Bird):
    @abstractmethod
    def swim():
        pass
class FlyingBird(Bird):
    @abstractmethod
    def flying():
        pass
    
class Sparrow(FlyingBird):
    def flying():
        pass
class Eagle(FlyingBird):
    def flying():
        pass
class Penguin(Bird):
    def move():
        pass
class Duck(SwimmingBird):
    def swim():
        pass