# ankur_portfolio

Simple Django portfolio project — ek app (`portfolio`) aur ek page (`index.html`)
jisme dummy profile details hain.

## Structure

```
ankur_portfolio/
├── manage.py
├── requirements.txt
├── ankur_portfolio/          # project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── portfolio/                # app
    ├── views.py              # dummy profile data yahan hai
    ├── urls.py
    └── templates/portfolio/index.html
```

## Chalane ka tarika

```bash
cd ankur_portfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Phir browser me: http://127.0.0.1:8000/

## Details badalni ho

`portfolio/views.py` me `PROFILE` dictionary edit kar do — page apne aap update ho jayega.
