import pprint
from typing import Any, Optional, final
from flask import Response, jsonify
from pymysql import Connection
from pymysql.cursors import DictCursor
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import InternalServerError, NotFound
from query import select_employee_view, select_employee_view_with_limit, select_employee_view_with_cursor_and_limit, select_employee_view_by_username_sql, delete_address_by_id_sql, delete_user_by_username_sql, insert_address_sql, insert_user_sql, insert_employee_sql
from helper import parse_cursor_pagination, parse_nested_json, parse_nested_json_from_list, hash_password

response_headers = {'content-type': 'application/json'}


def handle_fetch_one_employee(db_conn: Connection, username: str) -> Response:
    cursor: DictCursor = db_conn.cursor()

    try:
        cursor.execute(select_employee_view_by_username_sql, (username))
        result = cursor.fetchone()
        if result is None:
            raise NotFound(
                f"unable to find employee with username '{username}'")
        resp = parse_nested_json(result)
    except NotFound as e:
        raise e
    except Exception as e:
        raise InternalServerError(str(e))
    finally:
        cursor.close()

    return jsonify(resp), 200, response_headers


def handle_fetch_many_employee(db_conn: Connection, args: MultiDict[str, str]) -> Response:
    cursor: DictCursor = db_conn.cursor()
    pagination = parse_cursor_pagination(args)

    try:
        if pagination is None:
            cursor.execute(select_employee_view)
            result = cursor.fetchall()
        elif pagination['cursor'] is None:
            cursor.execute(select_employee_view_with_limit,
                           (pagination['limit']))
            result = cursor.fetchall()
        else:
            cursor.execute(select_employee_view_with_cursor_and_limit,
                           (pagination['cursor'], pagination['limit']))
            result = cursor.fetchall()
    except Exception as e:
        raise InternalServerError(str(e))
    finally:
        cursor.close()

    return jsonify(parse_nested_json_from_list(result)), 200, response_headers


def handle_create_one_employee(db_conn: Connection, body: Optional[Any]) -> Response:
    cursor: DictCursor = db_conn.cursor()

    # hash the password
    body['password_hash'] = hash_password(body['password'])
    del body['password']

    try:
        # get the department_id if it is specified
        if body['department'] is not None:
            cursor.execute(
                "SELECT department_id FROM department WHERE name = %s", body['department'])
            res = cursor.fetchone()
            if res is None:
                raise NotFound(
                    f"Unable to find department with name '{body['department']}'")
            department_id = res['department_id']

        # create the address if specified
        if body['address'] is not None:
            address = body['address']
            cursor.execute(insert_address_sql, tuple({
                'city': address['city'],
                'line1': address['line1'],
                'line2': address['line2'] if 'line2' in address else None,
                'state': address['state'],
                'country': address['country'],
                'postal_code': address['postal_code'],
            }.values()))
            address_id = cursor.lastrowid

        # create the user
        cursor.execute(insert_user_sql, tuple({
            'email': body['email'],
            'username': body['username'],
            'password_hash': body['password_hash'],
            'phone_number': body['phone_number'],
            'first_name': body['first_name'],
            'last_name': body['last_name'],
            'dob': body['dob'],
            'gender': body['gender'],
            'avatar_url': None
        }.values()))
        user_id = cursor.lastrowid

        # create the employee
        cursor.execute(insert_employee_sql, tuple({
            'salary': body['salary'] if 'salary' in body else 0,
            'role': body['role'],
            'start_at': body['start_at'],
            'end_at': body['end_at'] if 'end_at' in body else None,
            'user_id': user_id,
            'address_id': address_id if address_id is not None else None,
            'department_id': department_id if department_id is not None else None
        }.values()))

        # fetch the created employee
        cursor.execute(select_employee_view_by_username_sql, body['username'])
        result = cursor.fetchone()
        if result is None:
            raise Exception(
                f"Failed to fetch the created employee with username {body['username']}")
    except NotFound as e:
        db_conn.rollback()
        raise e
    except Exception as e:
        db_conn.rollback()
        raise InternalServerError(str(e))
    finally:
        db_conn.commit()
        cursor.close()

    return jsonify(result), 200, response_headers


def handle_update_one_employee(db_conn: Connection, username: str, body: Optional[Any]) -> Response:
    cursor: DictCursor = db_conn.cursor()

    try:
        # update the employee
        cursor.execute(update_employee_sql, tuple([*body.values(), username]))

        # fetch the updated employee
        cursor.execute(select_employee_view_by_username_sql, username)
        result = cursor.fetchone()
        if result is None:
            raise Exception(
                f"Failed to fetch the created employee with username {body['username']}")
    except Exception as e:
        db_conn.rollback()
        raise InternalServerError(str(e))
    finally:
        db_conn.commit()
        cursor.close()

    return jsonify(result), 200, response_headers


def handle_delete_one_employee(db_conn: Connection, username: str) -> Response:
    cursor: DictCursor = db_conn.cursor()

    try:
        # start transaction
        db_conn.begin()

        # fetch the employee
        cursor.execute(select_employee_view_by_username_sql, (username))
        result = cursor.fetchone()
        if result is None:
            raise NotFound(
                f"unable to find employee with username '{username}'")
        emp = parse_nested_json(result)

        # delete address if exist
        if 'address' in emp and 'address_id' in emp['address']:
            cursor.execute(delete_address_by_id_sql,
                           (emp['address']['address_id']))

        # delete the employee
        cursor.execute(delete_user_by_username_sql, emp['user']['user_id'])
    except NotFound as e:
        db_conn.rollback()
        raise e
    except Exception as e:
        db_conn.rollback()
        raise InternalServerError(str(e))
    finally:
        db_conn.commit()
        cursor.close()

    return jsonify(emp), 200, response_headers
