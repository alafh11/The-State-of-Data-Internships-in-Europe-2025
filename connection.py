import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

df = pd.read_csv(r"C:\Users\Alaa\Desktop\DataInternEu\cleaned_data_internships_eu.csv")

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


countries = df["country"].dropna().drop_duplicates()

for country in countries:
    try:
        cur.execute(
            "INSERT INTO countries (country_name) VALUES (%s) ON CONFLICT (country_name) DO NOTHING;",
            (country,),
        )
    except Exception as e:
        print(f"Error inserting country: {country} → {e}")

conn.commit()
print("✅ Countries inserted.")


city_country_pairs = df[["city", "country"]].dropna().drop_duplicates()

for _, row in city_country_pairs.iterrows():
    city = row["city"]
    country = row["country"]

    try:
        cur.execute(
            """
            INSERT INTO cities (city_name, country_name)
            VALUES (%s, %s)
            ON CONFLICT (city_name, country_name) DO NOTHING;
            """,
            (city, country),
        )
    except Exception as e:
        print(f"Error inserting city: {city}, country: {country} → {e}")

conn.commit()
print("✅ Cities inserted.")


company_info = df[["company_name", "city", "country"]].dropna().drop_duplicates()

for _, row in company_info.iterrows():
    company_name = row["company_name"]
    city = row["city"]
    country = row["country"]

    try:
        cur.execute(
            """
            INSERT INTO companies (company_name, city_name, country_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (company_name) DO NOTHING;
            """,
            (company_name, city, country),
        )
    except Exception as e:
        print(f"Error inserting company: {company_name} → {e}")

conn.commit()
print("✅ Companies inserted.")


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
print("✅ Job types inserted.")


clean_jobs = df.dropna(subset=["job_title", "company_name"]).drop_duplicates()

for idx, row in clean_jobs.iterrows():
    job_id = idx
    job_title = row["job_title"]
    company_name = row["company_name"]

    try:
        cur.execute(
            """
            INSERT INTO jobs (job_id, job_title, company_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (job_id) DO NOTHING;
            """,
            (job_id, job_title, company_name),
        )
    except Exception as e:
        print(f"Error inserting job ID {job_id} → {e}")

conn.commit()
print("✅ Jobs inserted.")
