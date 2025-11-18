import time
import concurrent.futures
from threading import Thread
from datetime import datetime, timedelta
import json
import os
import requests  # Added for potential ESP requests (currently commented)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# ESP configuration (commented for now)
ESP_IPS = [
    "http://10.110.105.38/",
    "http://10.110.105.39/"
]

# Track executed tasks to prevent duplicates
executed_tasks = set()

def run_task(schedule_obj, task_dt):
    """Send request to all ESPs for a given schedule (currently commented)."""
    task_key = (schedule_obj.id, task_dt.strftime('%Y-%m-%d %H:%M'))

    if task_key in executed_tasks:
        return  # Already executed

    # Determine endpoint based on bell_type
    if schedule_obj.bell_type == 0:
        endpoint = "supravatam1"
    elif schedule_obj.bell_type == 1:
        endpoint = "supravatam2"
    elif schedule_obj.bell_type == 2:
        endpoint = "normal"
    else:
        print(f"Invalid bell_type {schedule_obj.bell_type} for schedule {schedule_obj.id}")
        return

    # -----------------------------
    # Comment ESP requests for now
    # -----------------------------
    def send_request(esp_ip):
        try:
            r = requests.get(f"{esp_ip}{endpoint}", timeout=5)

            if r.status_code == 200:
                print(f"{schedule_obj.name} triggered on {esp_ip} at {datetime.now()}")
            print(f"{schedule_obj.name} triggered on {esp_ip} at {datetime.now()}")
      
        except Exception as e:
            print(f"ESP error {esp_ip}: {e}")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, ESP_IPS)

    # Instead, just print bell rang
    print(f"Bell rang for {schedule_obj.name} at {datetime.now()}")

    # >>> ADDED for bell log <<<
    log_bell_ring(schedule_obj)

    executed_tasks.add(task_key)


def check_schedules(db, Schedule):
    """Check DB for schedules and execute tasks if their time has arrived.
    Assumes called within an app context (no inner context push needed)."""
    now = datetime.now()
    next = now + timedelta(minutes=1)
    schedules = Schedule.query.all()
    for s in schedules:
        try:
            task_dt = datetime.strptime(f"{s.schedule_date} {s.schedule_time}", "%Y-%m-%d %H:%M:%S")
            if task_dt <= now:
                run_task(s, task_dt)
        except Exception as e:
            print(f"Invalid schedule format for schedule {s.id}: {e}")


def clear_past_schedules(db, Schedule):
    """Delete schedules whose datetime is in the past (already rung)."""
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    past_schedules = Schedule.query.filter(
        db.func.concat(Schedule.schedule_date, ' ', Schedule.schedule_time) <= now_str
    ).all()
    
    deleted_count = len(past_schedules)
    if deleted_count > 0:
        for s in past_schedules:
            db.session.delete(s)
        db.session.commit()
        print(f"Deleted {deleted_count} past schedules")
    else:
        pass


def start_scheduler(app, db, Schedule):
    def scheduler_thread():
        while True:
            try:
                with app.app_context():
                    check_schedules(db, Schedule)
                    clear_past_schedules(db, Schedule)
            except Exception as e:
                print(f"Scheduler error: {e}")
            time.sleep(1)

    t = Thread(target=scheduler_thread, daemon=True)
    t.start()


# Flask App
app = Flask(__name__)

# Database URI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "schedule.db")
DB_URI = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print(f"Database path: {os.path.normpath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///',''))}")


# ===========================
# DATABASE MODELS
# ===========================
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bell_type = db.Column(db.Integer, nullable=False)
    schedule_date = db.Column(db.String, nullable=False)
    schedule_time = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('schedule_date', 'schedule_time', name='unique_schedule_datetime'),
    )


class BellLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bell_type = db.Column(db.Integer, nullable=False)
    ring_time = db.Column(db.String, nullable=False, unique=True)
    date_logged = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


# >>> ADDED for bell log <<<
def log_bell_ring(schedule_obj):
    """Store info about a bell that has rung."""
    try:
        ring_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_log = BellLog(
            name=schedule_obj.name,
            bell_type=schedule_obj.bell_type,
            ring_time=ring_time,
            date_logged=schedule_obj.schedule_date
        )
        db.session.add(new_log)
        db.session.commit()
        print(f"Logged bell: {schedule_obj.name} at {ring_time}")
    except Exception as e:
        print(f"Error logging bell ring: {e}")


# ------------------------
# CREATE schedules (POST)
# ------------------------
@app.route('/schedules', methods=['POST'])
def save_schedule():
    try:
        data = request.json
        
        name = data.get('name')
        bell_type = data.get('bell_type')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        time_str = data.get('time')
        days = data.get('days')

        if not all([name, start_date, end_date, time_str, days]) or bell_type is None:
            return jsonify({'success': False, 'message': 'Missing required fields.'}), 400

        try:
            bell_type = int(bell_type)
            if bell_type not in [0, 1, 2]:
                raise ValueError
        except ValueError:
            return jsonify({'success': False, 'message': 'bell_type must be 0, 1, or 2.'}), 400

        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        hour, minute = map(int, time_str.split(':'))

        if isinstance(days, str):
            days = json.loads(days)
        days = list(map(int, days))

        current = start_dt
        schedules = []
        while current <= end_dt:
            if current.weekday() in days:
                ring_time = current.replace(hour=hour, minute=minute, second=0)
                schedule_date = ring_time.strftime("%Y-%m-%d")
                schedule_time = ring_time.strftime("%H:%M:%S")
                
                existing = Schedule.query.filter_by(
                    bell_type=bell_type,
                    schedule_date=schedule_date,
                    schedule_time=schedule_time
                ).first()
                
                if not existing:
                    schedules.append(Schedule(
                        name=name,
                        bell_type=bell_type,
                        schedule_date=schedule_date,
                        schedule_time=schedule_time
                    ))
                else:
                    print(f"Skipped duplicate: Bell Type {bell_type} on {schedule_date} at {schedule_time}")
            
            current += timedelta(days=1)

        if not schedules:
            return jsonify({'success': False, 'message': 'No new schedules to add (all were duplicates).'}), 400

        db.session.add_all(schedules)
        db.session.commit()

        for s in schedules:
            print(f"Inserted: {s.name} on {s.schedule_date} at {s.schedule_time} (Bell Type: {s.bell_type})")
        return jsonify({'success': True, 'message': f'Schedule saved successfully. Added {len(schedules)} new entries.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ------------------------
# DELETE schedule (DELETE)
# ------------------------
@app.route('/delete/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'success': False, 'message': 'Schedule not found'}), 404
        
        db.session.delete(schedule)
        db.session.commit()
        print(f"Deleted schedule: {schedule_id}")

        return jsonify({'success': True, 'message': f'Schedule {schedule_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ------------------------
# READ schedules (GET)
# ------------------------
@app.route('/schedules', methods=['GET'])
def get_schedules():
    try:
        sort_key = request.args.get('sort', 'schedule_date')
        sort_order = request.args.get('order', 'asc')
        bell_type_filter = request.args.get('bellType', None)

        if sort_key not in ['id', 'name', 'schedule_date', 'schedule_time', 'bell_type']:
            sort_key = 'schedule_date'

        order_col = getattr(Schedule, sort_key)
        if sort_order == 'desc':
            order_col = order_col.desc()

        query = Schedule.query
        if bell_type_filter is not None:
            try:
                bell_type_filter = int(bell_type_filter)
                query = query.filter(Schedule.bell_type == bell_type_filter)
            except ValueError:
                pass

        schedules = query.order_by(order_col).all()

        return jsonify([
            {
                'id': s.id,
                'name': s.name,
                'bell_type': s.bell_type,
                'schedule_date': s.schedule_date,
                'schedule_time': datetime.strptime(s.schedule_time, "%H:%M:%S").strftime("%I:%M %p")
            }
            for s in schedules
        ])
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# >>> ADDED for bell log viewing <<<
@app.route('/bell_log', methods=['GET'])
def get_bell_logs():
    """Fetch all bells that have rung."""
    try:
        sort_key = request.args.get('sort', 'id')
        sort_order = request.args.get('order', 'desc')

        order_col = getattr(BellLog, sort_key, BellLog.id)
        if sort_order == 'desc':
            order_col = order_col.desc()

        logs = BellLog.query.order_by(order_col).all()

        return jsonify([
            {
                'id': log.id,
                'name': log.name,
                'bell_type': log.bell_type,
                'ring_time':  datetime.strptime(log.ring_time, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
            if log.ring_time else None,
                'date_logged': log.date_logged
            }
            for log in logs
        ])
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    start_scheduler(app, db, Schedule)
    app.run(debug=True, port=5000)
