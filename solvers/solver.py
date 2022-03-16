from abc import ABC, abstractmethod

class Solver(ABC):
    @abstractmethod
    def solve(self, categories):
        pass

    @abstractmethod
    def get_name(self):
        pass