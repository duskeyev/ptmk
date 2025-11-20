from psycopg import connect  # pyright: ignore[reportMissingImports]
from typing import List
import os
from dotenv import load_dotenv  # type: ignore[import]

load_dotenv()

class DatabaseManager:
    
    def __init__(self):
        self.connection = connect(
            host=os.getenv('DB_HOST', 'localhost'),
            dbname=os.getenv('DB_NAME', 'employee_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', '5432')
        )
        self.connection.autocommit = False

    def clear_cache(self):
        # Временно включаем autocommit для DISCARD
        original = self.connection.autocommit
        self.connection.autocommit = True
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DISCARD ALL;")
        finally:
            self.connection.autocommit = original

    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    birth_date DATE NOT NULL,
                    gender VARCHAR(10) NOT NULL
                )
            """)
            self.connection.commit()
        print("Table created successfully")

    def insert_employee(self, employee):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (employee.full_name, employee.birth_date, employee.gender))
            employee_id = cursor.fetchone()[0]
            self.connection.commit()
            return employee_id

    def batch_insert_employees(self, employees: List):
        with self.connection.cursor() as cursor:
            data = [(emp.full_name, emp.birth_date, emp.gender) for emp in employees]
            cursor.executemany("""
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES (%s, %s, %s)
            """, data)
            self.connection.commit()
        print(f"Inserted {len(employees)} employees")

    def get_unique_employees_sorted(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT ON (full_name, birth_date) 
                       full_name, birth_date, gender
                FROM employees 
                ORDER BY full_name, birth_date
            """)
            return cursor.fetchall()

    def get_male_with_f_surname(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT full_name, birth_date, gender
                FROM employees 
                WHERE gender = 'male' AND full_name LIKE 'F%'
            """)
            return cursor.fetchall()

    #Индекс — это отдельная структура (B-tree), где Postgres заранее упорядочивает значения gender и full_name. Запрос WHERE gender='male' AND full_name LIKE 'F%' вместо полного скана в миллионы строк сразу прыгает к нужному диапазону и берёт только несколько страниц данных. мы строим вспомогательную структуру, чтобы выборка с узким фильтром выполнялась в разы быстрее.#

    def create_index(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_gender_full_name_prefix 
                ON employees (gender, full_name text_pattern_ops)
            """)
        self.connection.commit()

    def drop_index(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                DROP INDEX IF EXISTS idx_gender_full_name_prefix
            """)
        self.connection.commit()

    def analyze_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("ANALYZE employees;")

        self.connection.commit()

    def close(self):
        self.connection.close()