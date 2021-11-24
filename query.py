# INSERT
from typing import List


insert_department_sql = """
    INSERT INTO department (name, description) VALUES (%s, %s)
"""
insert_address_sql = """
    INSERT INTO address (
        city, 
        line1, 
        line2, 
        state, 
        country, 
        postal_code
    ) VALUES (
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    )
"""
insert_user_sql = """
    INSERT INTO user (
        email,
        username,
        password_hash,
        phone_number,
        first_name,
        last_name,
        dob,
        gender,
        avatar_url
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
"""
insert_employee_sql = """
    INSERT INTO employee (
        salary,
        role,
        start_at,
        end_at,
        user_id,
        address_id,
        department_id
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
"""

# SELECT
select_employee_view_by_username_sql = """
    SELECT *
    FROM employee_view
    WHERE JSON_EXTRACT(user, '$.username') = %s
"""
select_employee_view_by_email_sql = """
    SELECT *
    FROM employee_view
    WHERE JSON_EXTRACT(user, '$.email') = %s
"""
select_employee_view = """
    SELECT *
    FROM employee_view
"""
select_employee_view_with_limit = """
    SELECT *
    FROM employee_view
    LIMIT %s
"""
select_employee_view_with_cursor_and_limit = """
    SELECT *
    FROM employee_view
    WHERE employee_id > %s
    LIMIT %s
"""

# DELETE
delete_address_by_id_sql = """
    DELETE FROM address
    WHERE address_id = %s
"""
delete_user_by_username_sql = """
    DELETE FROM user
    WHERE username = %s
"""

# UPDATE


def build_employee_view_update_query(params: List[str]) -> List[str]:
    if len(params) == 0:
        raise Exception("update params cannot be empty")

    queries = []

    # this construct the middle part of the query
    dynamic_update_params = "".join(map(lambda x: f"{x} = %s, ", params))[:-2]

    update_employee_sql = "UPDATE employee_view SET " + \
        dynamic_update_params + " WHERE JSON_EXTRACT(user, '$.username') = %s"

    return []


# columns in table
employee_columns = ['salary', 'role', 'start_at', 'end_at']
department_columns = ['name', 'description']
address_columns = ['city', 'line1', 'line2', 'state', 'country', 'postal_code']
user_columns = ['email', 'username', 'password_hash', 'phone_number',
                'first_name', 'last_name', 'dob', 'gender', 'avatar_url']
