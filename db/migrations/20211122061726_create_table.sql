-- migrate:up
CREATE TABLE user (
    user_id BIGINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash CHAR(82) NOT NULL,
    phone_number TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    avatar_url TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);
CREATE TABLE address (
    address_id BIGINT NOT NULL AUTO_INCREMENT,
    city TEXT NOT NULL,
    line1 TEXT NOT NULL,
    line2 TEXT,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    PRIMARY KEY(address_id)
);
CREATE TABLE department (
    department_id BIGINT NOT NULL AUTO_INCREMENT,
    department_name VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (department_id)
);
CREATE TABLE employee (
    employee_id BIGINT NOT NULL AUTO_INCREMENT,
    salary DECIMAL(10, 2) NOT NULL DEFAULT 0,
    role TEXT NOT NULL,
    start_at DATE NOT NULL,
    end_at DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL UNIQUE,
    address_id BIGINT,
    department_id BIGINT,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);
-- migrate:down
DROP TABLE employee;
DROP TABLE department;
DROP TABLE address;
DROP TABLE user;