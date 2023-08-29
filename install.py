import shutil
import subprocess
import os

def install_pip():
    try:
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-pip"], check=True)
        print("pip installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error installing pip:", e)
        return

def install_requirements():
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error installing requirements:", e)
        return

def main():
    # Install pip if not installed
    install_pip()

    # Install requirements from requirements.txt
    install_requirements()

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
