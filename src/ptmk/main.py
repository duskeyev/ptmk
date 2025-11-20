import sys
import time
from database import DatabaseManager
from models import Employee
from services import generate_random_employee, generate_specific_employees

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py 1")
        print("  python main.py 2 \"Ivanov Petr Sergeevich\" 2009-07-12 Male")
        print("  python main.py 3")
        print("  python main.py 4")
        print("  python main.py 5")
        print("  python main.py 6")
        print("  python main.py 7")
        return

    mode = sys.argv[1]
    db = DatabaseManager()

    try:
        if mode == "1":
            db.create_table()

        elif mode == "2":
            if len(sys.argv) != 5:
                print("Usage: python main.py 2 \"Full Name\" YYYY-MM-DD Gender")
                return

            employee = Employee(sys.argv[2], sys.argv[3], sys.argv[4])
            employee_id = employee.save_to_db(db)
            print(f"Employee added with ID: {employee_id}")
            print(f"Age: {employee.calculate_age()} years")

        elif mode == "3":
            employees = db.get_unique_employees_sorted()
            print(f"Found {len(employees)} unique employees:")
            for row in employees:
                emp = Employee(row[0], row[1].strftime('%Y-%m-%d'), row[2])
                print(f"{emp.full_name} | {emp.birth_date} | {emp.gender} | {emp.calculate_age()} years")

        elif mode == "4":
            print("Generating 1,000,000 random employees...")
            batch_size = 10000
            for i in range(100):
                print(f"Batch {i+1}/100...")
                employees = [generate_random_employee() for _ in range(batch_size)]
                db.batch_insert_employees(employees)
            
            print("Generating 100 male employees with F surname...")
            specific_employees = generate_specific_employees(100)
            db.batch_insert_employees(specific_employees)
            print("Database populated successfully")

        elif mode == "5":
            db.clear_cache()
            db.analyze_table()
            start_time = time.time()
            employees = db.get_male_with_f_surname()
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"Query executed in {execution_time:.4f} seconds")
            print(f"Found {len(employees)} employees")

        elif mode == "6":
            print("Dropping existing optimization index (if any)...")
            db.drop_index()
            
            db.clear_cache()
            db.analyze_table()
            runs = 10

            def measure_query(manager, executions: int):
                times = []
                for i in range(executions):
                    start_time = time.time()
                    manager.get_male_with_f_surname()
                    end_time = time.time()
                    times.append(end_time - start_time)
                return times
            
            print("Before optimization:")
            times_before = measure_query(db, runs)
            avg_before = sum(times_before) / runs
            for idx, duration in enumerate(times_before, start=1):
                print(f"  Run {idx}: {duration:.4f} seconds")
            print(f"Average time before: {avg_before:.4f} seconds")
            
            print("Creating index...")
            db.create_index()
            db.analyze_table()
            
            db.clear_cache()
            
            print("After optimization:")
            db_after = DatabaseManager()
            db_after.clear_cache()
            times_after = measure_query(db_after, runs)
            avg_after = sum(times_after) / runs
            for idx, duration in enumerate(times_after, start=1):
                print(f"  Run {idx}: {duration:.4f} seconds")
            print(f"Average time after: {avg_after:.4f} seconds")
            
            if avg_after > 0:
                print(f"Optimization result: {avg_before/avg_after:.2f}x faster")
            else:
                print("Optimization result: average after is zero, cannot compute speedup")

        elif mode == "7":
            print("Dropping optimization index...")
            db.drop_index()
            print("Index removed (if it existed)")

        else:
            print(f"Unknown mode: {mode}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
        extra_db = locals().get('db_after')
        if extra_db:
            extra_db.close()

if __name__ == "__main__":
    main()