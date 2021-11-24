-- migrate:up
CREATE VIEW employee_view AS
SELECT E.employee_id,
    E.salary,
    E.role,
    E.start_at,
    E.end_at,
    E.created_at,
    E.updated_at,
    JSON_OBJECT(
        'user_id',
        U.user_id,
        'email',
        U.email,
        'username',
        U.username,
        'phone_number',
        U.phone_number,
        'first_name',
        U.first_name,
        'last_name',
        U.last_name,
        'dob',
        U.dob,
        'gender',
        U.gender,
        'avatar_url',
        U.avatar_url,
        'created_at',
        U.created_at,
        'updated_at',
        U.updated_at
    ) AS user,
    JSON_OBJECT(
        'department_id',
        D.department_id,
        'name',
        D.name,
        'description',
        D.description,
        'created_at',
        D.created_at,
        'updated_at',
        D.updated_at
    ) AS department,
    JSON_OBJECT(
        'address_id',
        A.address_id,
        'city',
        A.city,
        'line1',
        A.line1,
        'line2',
        A.line2,
        'state',
        A.state,
        'country',
        A.country,
        'postal_code',
        A.postal_code
    ) AS address
FROM employee E
    INNER JOIN user U ON U.user_id = E.user_id
    INNER JOIN department D ON D.department_id = E.department_id
    INNER JOIN address A ON A.address_id = E.address_id;
-- migrate:down
DROP VIEW employee_view;