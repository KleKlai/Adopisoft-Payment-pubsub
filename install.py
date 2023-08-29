import shutil
import subprocess
import os

def main():
    # Copy .env.example to .env
    try:
        shutil.copy(".env.example", ".env")
        print(".env.example copied to .env")
    except Exception as e:
        print("Error copying .env.example:", e)
        return

    # Run pg_notify.py to import trigger and function
    try:
        subprocess.run(["python", "pg_notify.py"], check=True)
        print("pg_notify.py executed successfully")
    except subprocess.CalledProcessError as e:
        print("Error running pg_notify.py:", e)
        return

if __name__ == "__main__":
    main()