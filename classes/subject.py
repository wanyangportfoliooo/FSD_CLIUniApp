import random
from dataclasses import dataclass, field

@dataclass
class Subject:
    id: int = field(default_factory=lambda: random.randint(1, 999))
    mark: int = field(default_factory=lambda: random.randint(25, 100))
    grade: str = "N/A"

    def __post_init__(self):
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 75:
            return "D"
        elif self.mark >= 65:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "F"
