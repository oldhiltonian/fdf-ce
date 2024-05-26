#!/bin/bash

: <<'EOF'
Upon VM startup, manually set the following environment variables:

FLASK_SECRET_KEY
FLASK_ENV
FMP_API_KEY

Then run the following command from the home directory:
git clone https://github.com/oldhiltonian/fdf-ce.git && cd fdf-ce && chmod +x setup.sh && ./setup.sh

This will setup the VM environment, install dependencies, and start the application with Gunicorn.
EOF

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install UFW and allow necessary ports
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow 5000
echo "y" | sudo ufw enable

# Install dependencies
sudo apt install -y build-essential curl libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Install pyenv
curl https://pyenv.run | bash
echo -e '\n# Pyenv configuration' >> ~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

# Install Python 3.12.0 with pyenv
pyenv install -s 3.12.0
pyenv global 3.12.0

# Navigate into the project directory
cd fdf-ce

# Install Python dependencies
pip install -r requirements.txt

# Start the application with Gunicorn
nohup env FLASK_SECRET_KEY=$FLASK_SECRET_KEY FLASK_ENV=$FLASK_ENV FMP_API_KEY=$FMP_API_KEY gunicorn --workers 3 --bind 0.0.0.0:5000 app:app &