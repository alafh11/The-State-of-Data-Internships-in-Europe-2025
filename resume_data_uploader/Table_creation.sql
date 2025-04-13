-- Run this script in the PostgreSQL query tool to initialize the database schema.

CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_id INTEGER NOT NULL,
    UNIQUE (city_name, country_id),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) UNIQUE NOT NULL,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE job_types (
    job_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    job_title VARCHAR(200) NOT NULL,
    company_id INTEGER NOT NULL,
    job_type_id INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (job_type_id) REFERENCES job_types(job_type_id)
);
