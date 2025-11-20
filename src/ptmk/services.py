import random
from datetime import datetime, timedelta
from typing import List
from models import Employee

def generate_random_employee():
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", 
                  "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", 
                  "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                 "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    middle_name = random.choice(first_names)
    full_name = f"{last_name} {first_name} {middle_name}"
    
    end_date = datetime.now() - timedelta(days=365*18)
    start_date = end_date - timedelta(days=365*47)
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    gender = random.choice(["male", "female"])
    
    return Employee(full_name, birth_date, gender)

def generate_specific_employees(count: int = 100):
    first_names = ["Frank", "Fred", "Felix", "Ford", "Finn"]
    f_last_names = ["Fisher", "Foster", "Ford", "Fletcher", "Franklin"]
    
    employees = []
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(f_last_names)
        middle_name = random.choice(first_names)
        full_name = f"{last_name} {first_name} {middle_name}"
        
        end_date = datetime.now() - timedelta(days=365*20)
        start_date = end_date - timedelta(days=365*40)
        random_days = random.randint(0, (end_date - start_date).days)
        birth_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        employees.append(Employee(full_name, birth_date, "male"))
    
    return employees