# PARALLAX — Django Web Application

> **Shift Perspectives. Build the Future.**  
> Official website for the Parallax Hackathon — Home & About pages.

---

## Quick Start

```bash
# 1. Clone / unzip the project
cd parallax_django

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy env file and set your secret key
cp .env.example .env
# edit .env → set SECRET_KEY

# 5. Apply migrations
python manage.py migrate

# 6. Seed initial content (tracks, team, stats, values)
python manage.py seed_data

# 7. (Optional) Create admin superuser
python manage.py createsuperuser

# 8. Run the dev server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.  
Django Admin: **http://127.0.0.1:8000/admin/**

---

## Project Structure

```
parallax_django/
├── manage.py
├── requirements.txt
├── .env.example
│
├── parallax/               ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                   ← Main app
│   ├── models.py           ← Stat, Track, Value, TeamMember
│   ├── views.py            ← home(), about()
│   ├── urls.py             ← / and /about/
│   ├── admin.py            ← Admin panel config
│   ├── migrations/
│   └── management/
│       └── commands/
│           └── seed_data.py  ← python manage.py seed_data
│
├── templates/
│   ├── base.html           ← Nav + footer + blocks
│   ├── home.html           ← Hero, ticker, tracks, why, CTA
│   └── about.html          ← Hero, mission, story, values, team
│
└── static/
    ├── css/parallax.css    ← Full brand stylesheet
    └── js/main.js          ← Scroll reveal + parallax effect
```

---

## URLs

| URL        | View    | Template      |
|------------|---------|---------------|
| `/`        | `home`  | `home.html`   |
| `/about/`  | `about` | `about.html`  |
| `/admin/`  | Django admin panel    |

---

## Content Management

All content is managed through **Django Admin** (`/admin/`).  
No code changes needed to update tracks, team members, values, or stats.

| Model        | Purpose                        |
|-------------|--------------------------------|
| `Track`      | Hackathon challenge tracks     |
| `TeamMember` | About page team cards          |
| `Value`      | About page values grid         |
| `Stat`       | Home page ticker numbers       |

---

## Design System

| Token         | Value       | Usage                          |
|---------------|-------------|-------------------------------|
| `--blue`      | `#0052CC`   | CTAs, geometry, borders        |
| `--cyan`      | `#00D9FF`   | Glows, hovers, accents         |
| `--glow`      | `#1EFFF0`   | Bright highlights, orb core    |
| `--bg`        | `#0A0E27`   | Main background                |
| `--card`      | `#1A1F3A`   | Cards, alternate sections      |
| `--border`    | `#2A3050`   | Card borders, dividers         |
| `--muted`     | `#B0B8D4`   | Secondary text                 |
| Glassmorphism | `rgba(26,31,58,0.6)` + `backdrop-filter:blur(12px)` |

---

## Production Deployment

```bash
# Collect static files (served by WhiteNoise)
python manage.py collectstatic

# Set in .env:
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com
```
