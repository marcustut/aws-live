import csv
from typing import List, OrderedDict
from faker import Faker
from pymysql import connections
from argon2 import PasswordHasher
from config import Config
from query import insert_employee_sql, insert_address_sql, insert_user_sql, insert_department_sql

# initialize faker instance
fake = Faker()

# initialize password hasher
ph = PasswordHasher()

# initialize the config (setup environment var)
config = Config()

# connect to rds (mysql)
db_conn = connections.Connection(
    host=config.database_host,
    port=3306,
    user=config.database_user,
    password=config.database_password,
    db=config.database_db
)

# constants
NUM_DEPARTMENT = 5
NUM_EMPLOYEES = 50

FAKE_USER_CSV = "./fake_user.csv"


# generate fake users
fake_users = [{
    "email": fake.email(),
    "username": fake.simple_profile()['username'],
    "password_hash": fake.password(),
    "phone_number": fake.phone_number(),
    "first_name": fake.first_name(),
    "last_name": fake.last_name(),
    "dob": fake.date_of_birth(maximum_age=50),
    "gender": 'male' if fake.simple_profile()['sex'] == 'M' else 'female',
    "avatar_url": fake.image_url(),
} for _ in range(NUM_EMPLOYEES)]

fake_department_ids: List[int] = []


# insert fake data into `department` table
def seed_department():
    cursor = db_conn.cursor()
    try:
        for _ in range(NUM_DEPARTMENT):
            cursor.execute(insert_department_sql,
                           (fake.city(), fake.sentence()))
            fake_department_ids.append(cursor.lastrowid)
            print(f"seed `department` with id {cursor.lastrowid} - SUCCESS ✅")
    except Exception as e:
        raise e
    finally:
        db_conn.commit()
        cursor.close()


# insert fake data into `address` table
def seed_address():
    cursor = db_conn.cursor()
    try:
        for fake_user in fake_users:
            cursor.execute(
                insert_address_sql,
                (fake.city(), fake.street_address(), fake.random_element(elements=OrderedDict([(fake.street_name(), 0.3), (None, 0.7)])),
                 fake.state(), fake.country(), fake.postcode()))
            fake_user['address_id'] = cursor.lastrowid
            print(f"seed `address` with id {cursor.lastrowid} - SUCCESS ✅")
    except Exception as e:
        raise e
    finally:
        db_conn.commit()
        cursor.close()


# insert fake data into `user` table
def seed_user():
    # hash the password
    for fake_user in fake_users:
        fake_user['password_hash'] = ph.hash(fake_user['password_hash'])

    # insert user and get the user_id
    cursor = db_conn.cursor()
    try:
        for fake_user in fake_users:
            cursor.execute(
                insert_user_sql,
                (fake_user['email'], fake_user['username'], fake_user['password_hash'], fake_user['phone_number'],
                 fake_user['first_name'], fake_user['last_name'], fake_user['dob'], fake_user['gender'], fake_user['avatar_url'])
            )
            fake_user['user_id'] = cursor.lastrowid
            print(f"seed `user` with id {cursor.lastrowid} - SUCCESS ✅")
    except Exception as e:
        raise e
    finally:
        db_conn.commit()
        cursor.close()


# insert fake data into `employee` table
def seed_employee():
    # generate fake employee data
    fake_employees = [{
        'salary': fake.random_int(min=2000, max=9999),
        'role': fake.random_element(elements=('manager', 'admin', 'cashier', 'runner')),
        'start_at': fake.date_between(start_date=fake_user['dob']),
        'end_at': None,
        'user_id': fake_user['user_id'],
        'address_id': fake_user['address_id'],
        'department_id': fake.random_element(elements=tuple(fake_department_ids))
    } for fake_user in fake_users]
    # update the 'end_at' to be after 'start_at'
    for fake_employee in fake_employees:
        fake_employee['end_at'] = fake.random_element(elements=OrderedDict(
            [(fake.date_between(start_date=fake_employee['start_at']), 0.3), (None, 0.7)])),

    cursor = db_conn.cursor()
    try:
        for fake_employee in fake_employees:
            cursor.execute(insert_employee_sql, tuple(fake_employee.values()))
            print(f"seed `employee` with id {cursor.lastrowid} - SUCCESS ✅")
    except Exception as e:
        raise e
    finally:
        db_conn.commit()
        cursor.close()


def seed():
    seed_department()
    seed_address()
    seed_user()
    seed_employee()


def clean():
    cursor = db_conn.cursor()
    try:
        cursor.execute("DELETE FROM employee")
        cursor.execute("DELETE FROM user")
        cursor.execute("DELETE FROM department")
        cursor.execute("DELETE FROM address")
        print(f"clean `employee` - SUCCESS ✅")
        print(f"clean `user` - SUCCESS ✅")
        print(f"clean `department` - SUCCESS ✅")
        print(f"clean `address` - SUCCESS ✅")
    except Exception as e:
        raise e
    finally:
        db_conn.commit()
        cursor.close()


if __name__ == "__main__":
    # save fake_user login credentials to a csv file
    with open(FAKE_USER_CSV, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['username', 'password'])
        writer.writeheader()
        for fake_user in fake_users:
            writer.writerow(
                {'username': fake_user['username'], 'password': fake_user['password_hash']})

    # clean the db
    clean()

    # seed the db
    seed()
