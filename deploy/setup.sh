#!/usr/bin/env bash
# EC2 (Ubuntu) par ek baar chalao: bash deploy/setup.sh
# Maan ke chal raha hai ki repo /home/ubuntu/ankur_portfolio me clone hai.
set -euo pipefail

APP_DIR=/home/ubuntu/ankur_portfolio
cd "$APP_DIR"

sudo apt update
sudo apt install -y python3-venv python3-pip nginx

python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
    SECRET=$(venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(50))')
    PUBLIC_IP=$(curl -s https://checkip.amazonaws.com || echo "")
    cat > .env <<ENV
DJANGO_SECRET_KEY=$SECRET
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$PUBLIC_IP,localhost,127.0.0.1
ENV
    echo ".env bana di (ALLOWED_HOSTS=$PUBLIC_IP). Domain ho to .env me add kar dena."
fi

set -a; source .env; set +a
venv/bin/python manage.py migrate --noinput
venv/bin/python manage.py collectstatic --noinput

# nginx (www-data) ko home dir ke andar static files padhne do
chmod 755 /home/ubuntu

sudo cp deploy/gunicorn.socket /etc/systemd/system/gunicorn.socket
sudo cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn.socket
sudo systemctl restart gunicorn

sudo cp deploy/nginx.conf /etc/nginx/sites-available/ankur_portfolio
sudo ln -sf /etc/nginx/sites-available/ankur_portfolio /etc/nginx/sites-enabled/ankur_portfolio
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "Done! Browser me kholo: http://${PUBLIC_IP:-<EC2_PUBLIC_IP>}/"
