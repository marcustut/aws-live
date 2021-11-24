email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
msia_phone_regex = r'^(\+?6?01)[0|1|2|3|4|6|7|8|9]\-*[0-9]{7,8}$'
gender_regex = r'^(male|female)$'
base64_image_regex = r'(data:image\/[^;]+;base64[^"]+)'
date_regex = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'

create_or_update_employee_base_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'pattern': email_regex},
        'username': {'type': 'string', 'minLength': 4},
        'password': {'type': 'string', 'minLength': 8},
        'phone_number': {'type': 'string', 'pattern': msia_phone_regex},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'gender': {'type': 'string', 'pattern': gender_regex},
        'dob': {'type': 'string', 'pattern': date_regex},
        'salary': {'type': 'number', 'minimum': 0},
        'role': {'type': 'string'},
        'start_at': {'type': 'string', 'pattern': date_regex},

        'end_at': {'type': 'string', 'pattern': date_regex},
        'avatar_image': {'type': 'string', 'pattern': base64_image_regex},
        'address': {
            'type': 'object',
            'properties': {
                'city': {'type': 'string'},
                'line1': {'type': 'string'},
                'line2': {'type': 'string'},
                'state': {'type': 'string'},
                'country': {'type': 'string'},
                'postal_code': {'type': 'string', 'minLength': 5, 'maxLength': 5},
            },
            'required': ['city', 'line1', 'state', 'country', 'postal_code']
        },
        'department': {'type': 'string'}
    },
}

create_employee_schema = {
    'type': create_or_update_employee_base_schema['type'],
    'properties': create_or_update_employee_base_schema['properties'],
    'required': [
        'email',
        'username',
        'password',
        'phone_number',
        'first_name',
        'last_name',
        'gender',
        'dob',
        'role',
        'start_at'
    ]
}

update_employee_schema = {
    'type': create_or_update_employee_base_schema['type'],
    'properties': create_or_update_employee_base_schema['properties'],
    'required': []
}
