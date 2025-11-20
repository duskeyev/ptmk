from datetime import datetime

class Employee:
    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender.lower()

    def calculate_age(self):
        birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age

    def save_to_db(self, db):
        return db.insert_employee(self)