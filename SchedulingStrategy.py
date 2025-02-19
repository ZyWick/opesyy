from abc import ABC, abstractmethod

class SchedulingStrategy(ABC):
    @abstractmethod
    def execute(self, process_array, quantum_value=1):
        pass