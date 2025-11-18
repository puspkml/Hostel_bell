# Hostel Bell Automation System

A full-stack automation system for scheduling, triggering, and logging bells in hostels, schools, and institutions.

This project uses:

- **SvelteKit + TailwindCSS** → Frontend UI  
- **Flask + SQLite + Background Thread** → Backend scheduler  
- **Optional ESP NodeMCU devices** → Bell triggering via HTTP requests  

---

## Features

- Create bell schedules with date ranges and weekday filters  
- Prevents duplicate schedule entries  
- Real-time background scheduler (Python thread)  
- Logs every triggered bell event  
- REST API for schedules & logs  
- Modern UI built with SvelteKit  
- Manual bell control page  
- Calendar view for schedules  

---

## Project Structure

```
root/
│
├── bell.py                # Flask backend + scheduler logic
├── schedule.db            # SQLite database
├── requirements.txt       # Backend dependencies
│
├── package.json           # SvelteKit dependencies
├── svelte.config.js
├── tailwind.config.ts
├── vite.config.ts
│
├── src/
│   ├── lib/
│   │   ├── assets/
│   │   │   └── favicon.svg
│   │   ├── components/
│   │   │   ├── Navbar.svelte
│   │   │   └── Footer.svelte
│   │   └── utils/
│   │       ├── date.ts
│   │       └── socket.ts
│   │
│   ├── routes/
│   │   ├── scheduler/
│   │   ├── calendar/
│   │   ├── past_bells/
│   │   ├── manual_control/
│   │   ├── About/
│   │   └── api/
│   │
│   ├── +layout.svelte
│   └── +page.svelte
│
└── static/
```

---

## Backend Setup (Flask)

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run the server
```
python bell.py
```

Backend will run at:
```
http://localhost:5000
```

The scheduler thread automatically starts and checks schedules every second.

---

## Frontend Setup (SvelteKit)

### 1. Install dependencies
```
npm install
```

### 2. Start development server
```
npm run dev
```

Runs at:
```
http://localhost:5173
```

---

## REST API Endpoints

### Create schedule
```
POST /schedules
```
Body:
```json
{
  "name": "Morning Bell",
  "bell_type": 2,
  "startDate": "2025-02-01",
  "endDate": "2025-02-05",
  "time": "06:30",
  "days": [1,2,3,4,5]
}
```

### Get schedules
```
GET /schedules
```

### Delete schedule
```
DELETE /delete/<id>
```

### Get bell logs
```
GET /bell_log
```

---

## How the Scheduler Works

- Python thread runs every second  
- Compares current time with DB schedule entries  
- If due → triggers bell:  
  - Sends ESP request (optional)  
  - Saves log entry  
- Deletes past schedules automatically  

---

## ESP Integration (Optional)

ESP IPs are listed in `bell.py`:
```
ESP_IPS = [
  "http://10.110.231.128/"
]
```

Endpoints triggered:
```
/supravatam1
/supravatam2
/normal
```

---

## Requirements (requirements.txt)

```
Flask
Flask-SQLAlchemy
requests
```

---

## Notes

- SQLite is used locally; can be upgraded to PostgreSQL/MySQL  
- SvelteKit is fully compatible with Vercel deployment  
- Python backend can run on Gunicorn, PM2, Systemd, or Docker  

---

## Acknowledgement

This project is lovingly dedicated to **Bhagawan Sri Sathya Sai Baba**.  
It was implemented with heartfelt devotion on the sacred occasion of **Bhagawan’s 100th Birthday**.

We express our sincere gratitude to:

- **Hursh Gupta** – for invaluable technical guidance and continuous support.  
- **Sundarmurty Sir** – for mentorship, encouragement, and facilitating the project.  
- **Dr. Sumukh Nandan** – for providing insights, oversight, and support throughout the development.  
- **Bhagawan Sri Sathya Sai Baba** – whose divine inspiration, love, and blessings made this project possible.

With humility and gratitude,  
*We offer this work at His Divine Lotus Feet.*

