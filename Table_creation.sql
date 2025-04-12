CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_id INTEGER REFERENCES countries(country_id),
    UNIQUE (city_name, country_id)
);

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE job_types (
    job_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    job_title VARCHAR(200) NOT NULL,
    company_id INTEGER REFERENCES companies(company_id),
    city_id INTEGER REFERENCES cities(city_id),
    job_type_id INTEGER REFERENCES job_types(job_type_id),
);