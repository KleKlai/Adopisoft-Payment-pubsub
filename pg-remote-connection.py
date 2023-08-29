import subprocess

def modify_postgresql_config():
    # Update postgresql.conf to allow remote connections
    subprocess.run(["sudo", "sed", "-i", "s/#listen_addresses = 'localhost'/listen_addresses = '*'/", "/etc/postgresql/12/main/postgresql.conf"], check=True)

    # Add a new entry to pg_hba.conf to allow remote connections
    with open("/etc/postgresql/12/main/pg_hba.conf", "a") as f:
        f.write("\n# Allow remote connections\nhost    all             all             0.0.0.0/0            md5\n")

    # Restart PostgreSQL to apply changes
    subprocess.run(["sudo", "service", "postgresql", "restart"], check=True)

if __name__ == "__main__":
    modify_postgresql_config()
