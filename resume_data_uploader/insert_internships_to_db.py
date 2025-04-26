import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

df = pd.read_csv(filepath)

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    print("Successfully connected to PostgreSQL!")
except psycopg2.Error as e:
    print("Connection failed.")
    print(e)

cur = conn.cursor()

# -------------------------------
countries = df["country"].dropna().drop_duplicates()

for country in countries:
    try:
        cur.execute(
            """
            INSERT INTO countries (country_name)
            VALUES (%s)
            ON CONFLICT (country_name) DO NOTHING;
        """,
            (country,),
        )
    except Exception as e:
        print(f"Error inserting country: {country} → {e}")

conn.commit()
print("Countries inserted.")

# -------------------------------
city_country_pairs = df[["city", "country"]].dropna().drop_duplicates()

for _, row in city_country_pairs.iterrows():
    city = row["city"]
    country = row["country"]

    try:
        cur.execute(
            "SELECT country_id FROM countries WHERE country_name = %s;", (country,)
        )
        country_id = cur.fetchone()
        if country_id:
            cur.execute(
                """
                INSERT INTO cities (city_name, country_id)
                VALUES (%s, %s)
                ON CONFLICT (city_name, country_id) DO NOTHING;
            """,
                (city, country_id[0]),
            )
    except Exception as e:
        print(f"Error inserting city: {city}, {country} → {e}")

conn.commit()
print("Cities inserted.")

# -------------------------------
company_info = df[["company_name", "city", "country"]].dropna().drop_duplicates()

for _, row in company_info.iterrows():
    company_name = row["company_name"]
    city = row["city"]
    country = row["country"]

    try:
        cur.execute(
            """
            SELECT country_id FROM countries WHERE country_name = %s;
        """,
            (country,),
        )
        country_id = cur.fetchone()

        if not country_id:
            print(f"Country not found: {country}")
            continue

        cur.execute(
            """
            SELECT city_id FROM cities WHERE city_name = %s AND country_id = %s;
        """,
            (city, country_id[0]),
        )
        city_id = cur.fetchone()

        if city_id:
            cur.execute(
                """
                INSERT INTO companies (company_name, city_id)
                VALUES (%s, %s)
                ON CONFLICT (company_name) DO NOTHING;
            """,
                (company_name, city_id[0]),
            )
    except Exception as e:
        print(f"Error inserting company: {company_name} → {e}")

conn.commit()
print("Companies inserted.")

# -------------------------------
job_types = df["job_type"].dropna().drop_duplicates()

for job_type in job_types:
    try:
        cur.execute(
            """
            INSERT INTO job_types (type_name)
            VALUES (%s)
            ON CONFLICT (type_name) DO NOTHING;
        """,
            (job_type,),
        )
    except Exception as e:
        print(f"Error inserting job type: {job_type} → {e}")

conn.commit()
print("Job types inserted.")

# -------------------------------
clean_jobs = df.dropna(subset=["job_title", "company_name"]).drop_duplicates()

for idx, row in clean_jobs.iterrows():
    job_title = row["job_title"]
    company_name = row["company_name"]
    job_type = row["job_type"]

    try:
        cur.execute(
            "SELECT company_id FROM companies WHERE company_name = %s;", (company_name,)
        )
        company_id = cur.fetchone()
        if not company_id:
            print(f"Company not found for job: {job_title}")
            continue

        job_type_id = None
        if pd.notna(job_type):
            cur.execute(
                "SELECT job_type_id FROM job_types WHERE type_name = %s;", (job_type,)
            )
            result = cur.fetchone()
            if result:
                job_type_id = result[0]

        cur.execute(
            """
            INSERT INTO jobs (job_title, company_id, job_type_id)
            VALUES (%s, %s, %s);
        """,
            (job_title, company_id[0], job_type_id),
        )

    except Exception as e:
        print(f"Error inserting job '{job_title}' → {e}")

conn.commit()
print("Jobs inserted.")

cur.close()
conn.close()
print("Done wiyouuuu")
