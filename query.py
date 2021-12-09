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

# columns in table
employee_columns = ['salary', 'role', 'start_at', 'end_at']
department_columns = ['name', 'description']
address_columns = ['city', 'line1', 'line2', 'state', 'country', 'postal_code']
user_columns = ['email', 'username', 'password_hash', 'phone_number',
                'first_name', 'last_name', 'dob', 'gender', 'avatar_url']

def build_employee_view_update_query(username: str, params: List[str]) -> tuple[str, str, str, str]:
    if len(params) == 0:
        raise Exception("update params cannot be empty")

    employee_params = [p for p in params if p in employee_columns]
    user_params = [p for p in params if p in user_columns]
    department_params = [p for p in params if p in department_columns]
    address_params = [p for p in params if p in address_columns]

    update_employee_sql = "UPDATE `employee` AS e, `user` AS u SET " + \
            _get_dynamic_update_params(employee_params) + f" WHERE e.user_id = u.user_id AND u.username = %s"

    update_user_params = "UPDATE `user` SET " + \
            _get_dynamic_update_params(user_params) + f" WHERE username = %s"

    update_department_params = "UPDATE `department` AS d, `user` AS u, `employee` AS e SET " + \
            _get_dynamic_update_params(department_params) + f" WHERE u.username = %s AND u.user_id = e.user_id AND e.department_id = d.department_id"

    update_address_params = "UPDATE `address` AS a, `user` AS u, `employee` AS e SET " + \
            _get_dynamic_update_params(address_params) + f" WHERE u.username = %s AND u.user_id = e.user_id AND e.department_id = d.department_id"

    return update_employee_sql, update_user_params, update_department_params, update_address_params

def _get_dynamic_update_params(params: List[str]) -> str:
    # this construct the middle part of the query
    return "".join(map(lambda x: f"{x} = %s, ", params))[:-2]
