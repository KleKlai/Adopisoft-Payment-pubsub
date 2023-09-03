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
    pip install -r requirements.txt
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
    cat <<EOF > /etc/systemd/system/adopisoft-payment-notification.service
[Unit]
Description=Adopisoft payment notification collection agent service
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
    systemctl enable adopisoft-payment-notification
    systemctl start adopisoft-payment-notification

    echo "Systemd service configured and started."
}

# Main function
main() {
    # Install requirements from requirements.txt within the virtual environment
    install_requirements

    # Copy .env.example to .env
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ".env.example copied to .env"
    else
        echo "Error: .env.example not found."
        exit 1
    fi

    # Run pg_notify.py to import trigger and function
    if [ -f pg_notify.py ]; then
        python pg_notify.py
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