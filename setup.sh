#!/bin/bash
set -e

# Check for Python 2
if command -v python &>/dev/null; then
    echo "Python is installed."
else
    echo "Python is not installed."
fi

# Function to install requirements in the virtual environment
install_requirements() {
    pip install -r /usr/bin/adopaynotif/requirements.txt
    if [ $? -eq 0 ]; then
        echo "Requirements installed successfully."
    else
        echo "Error: Requirements installation failed."
        exit 1
    fi
}

# Function to configure and start the systemd service
configure_systemd_service() {
    # Create the systemd service file
    cat <<EOF > /etc/systemd/system/adopaynotif.service
[Unit]
Description=Adopaynotif is a server-based agent for collecting and sending payment events
After=network.target

[Service]
ExecStart=/usr/bin/python /usr/bin/adopaynotif/payment_notification_producer_v2.py
WorkingDirectory=/usr/bin/adopaynotif
Restart=always
User=adoadmin
Group=adoadmin

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd configuration
    systemctl daemon-reload

    # Enable and start the systemd service
    systemctl enable adopaynotif
    systemctl start adopaynotif

    echo "Systemd service configured and started."
}

create_env() {

    # Create .env file
    cat <<EOF > # Database Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "adopisoft"
DB_USER = "adopisoft"
DB_PASSWORD = "adopisoft"

# Google Cloud Pub/Sub Configuration
GOOGLE_APPLICATION_CREDENTIALS = "./privatekey.json"

EOF

    echo ".env has been created."
}

# Main function
main() {
    # Install requirements from requirements.txt within the virtual environment
    install_requirements

    # Create env file
    create_env

    # Run pg_notify.py to import trigger and function
    if [ -f /usr/bin/adopaynotif/pg_notify.py ]; then
        python /usr/bin/adopaynotif/pg_notify.py
        echo "pg_notify.py executed successfully."
    else
        echo "Error: pg_notify.py not found."
        exit 1
    fi

    # Configure and start the systemd service
    configure_systemd_service
}

# Execute the main function
main