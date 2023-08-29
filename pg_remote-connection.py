import subprocess

def modify_postgresql_config():
    # Update postgresql.conf to allow remote connections
    subprocess.call(["sudo", "sed", "-i", "s/#listen_addresses = 'localhost'/listen_addresses = '*'/", "/etc/postgresql/10/main/postgresql.conf"])

    # Add a new entry to pg_hba.conf to allow remote connections
    with open("/etc/postgresql/10/main/pg_hba.conf", "a") as f:
        f.write("\n# Allow remote connections\nhost    all             all             0.0.0.0/0            md5\n")

    # Restart PostgreSQL to apply changes
    subprocess.call(["sudo", "service", "postgresql", "restart"])

if __name__ == "__main__":
    modify_postgresql_config()
