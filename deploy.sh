#!/bin/bash
# Server par naya code deploy karo.
# Use: cd ~/ankur_portfolio && ./deploy.sh

set -e

APP_DIR=/home/ubuntu/ankur_portfolio

echo "==> 1. Project folder me ja rahe hain"
cd $APP_DIR

echo "==> 2. Latest code la rahe hain (git pull)"
git pull

echo "==> 3. venv activate"
source venv/bin/activate

echo "==> 4. Packages install"
pip install -r requirements.txt

echo "==> 5. .env load"
set -a
source .env
set +a

echo "==> 6. Database migrate"
python manage.py migrate --noinput

echo "==> 7. Static files collect"
python manage.py collectstatic --noinput

echo "==> 8. Gunicorn restart"
sudo systemctl restart gunicorn

echo "==> 9. Health check"
sleep 3
curl -f -s -o /dev/null --unix-socket /run/gunicorn.sock http://localhost/

echo "✅ Deploy successful: $(git log -1 --oneline)"
