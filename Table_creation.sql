CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    UNIQUE (city_name, country_name)
);

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) UNIQUE NOT NULL,
    city_name VARCHAR(100),
    country_name VARCHAR(100)
);

CREATE TABLE job_types (
    job_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    job_title VARCHAR(200) NOT NULL,
    company_name VARCHAR(100) NOT NULL
);
