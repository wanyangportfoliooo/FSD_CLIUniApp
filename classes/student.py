import random
from dataclasses import dataclass, field

from classes.subject import Subject

@dataclass
class Student:
    email: str
    name: str
    id: str = field(default_factory=lambda: f"{random.randint(1, 999999):06d}")
    subjects: list = field(default_factory=list)
    mark: float = 0.0

    def regenerate_id(self):
        self.id = f"{random.randint(1, 999999):06d}"

    def enrol_subject(self):
        new_subject = Subject()
        self.subjects.append(new_subject)
        self.calculate_average()
        return new_subject

    def remove_subject(self, sid):
        for subject in self.subjects:
            if subject.id == sid:
                self.subjects.remove(subject)
                self.calculate_average()
                return True
        return False

    def calculate_average(self):
        if not self.subjects:
            self.mark = 0.0
            return 0.0
        total_mark = sum(subject.mark for subject in self.subjects)
        self.mark = total_mark / len(self.subjects)
        return self.mark

    def get_grade(self):
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
