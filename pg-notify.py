import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

# SQL statements to create the trigger function and trigger
sql_trigger_function = """
CREATE OR REPLACE FUNCTION notify_new_payment()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify('payment_notification', row_to_json(NEW)::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

sql_create_trigger = """
CREATE TRIGGER payment_insert_trigger
AFTER INSERT ON payments
FOR EACH ROW
EXECUTE PROCEDURE notify_new_payment();
"""

def add_trigger_and_function():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute(sql_trigger_function)
        cursor.execute(sql_create_trigger)

        connection.commit()
        print("Trigger function and procedure created successfully.")
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    add_trigger_and_function()
