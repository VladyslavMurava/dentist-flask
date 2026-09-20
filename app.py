import os
from datetime import date

import psycopg2
import psycopg2.extras
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
app.json.ensure_ascii = False

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)


def init_db():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                price INTEGER NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                patient_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                service_id INTEGER NOT NULL REFERENCES services(id),
                visit_date DATE NOT NULL,
                comment TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """)
        cur.execute("SELECT COUNT(*) AS n FROM services")
        if cur.fetchone()["n"] == 0:
            cur.executemany(
                "INSERT INTO services (name, price) VALUES (%s, %s)",
                [
                    ("Консультація", 0),
                    ("Лікування карієсу", 1200),
                    ("Професійна гігієна", 1500),
                    ("Відбілювання", 4500),
                    ("Протезування", 7000),
                    ("Дитяча стоматологія", 800),
                ],
            )


def fetch_services():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, price FROM services ORDER BY id")
        return cur.fetchall()


@app.route("/")
def index():
    return render_template("index.html", services=fetch_services(), today=date.today().isoformat())


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("patient_name", "").strip()
    phone = request.form.get("phone", "").strip()
    service_id = request.form.get("service_id", "")
    visit_date = request.form.get("visit_date", "")
    comment = request.form.get("comment", "").strip()

    if not name or not phone or not service_id or not visit_date:
        flash("Заповніть усі обов'язкові поля.", "error")
        return redirect(url_for("index"))

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO appointments (patient_name, phone, service_id, visit_date, comment)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (name, phone, service_id, visit_date, comment or None),
        )
        new_id = cur.fetchone()["id"]

    flash(f"Дякуємо, {name}! Ваша заявка №{new_id} прийнята, ми зателефонуємо для підтвердження.", "success")
    return redirect(url_for("index"))


@app.route("/appointments")
def appointments():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT a.id, a.patient_name, a.phone, s.name AS service, s.price,
                   a.visit_date, a.comment, a.created_at
            FROM appointments a
            JOIN services s ON s.id = a.service_id
            ORDER BY a.visit_date, a.id
        """)
        rows = cur.fetchall()
    return render_template("appointments.html", appointments=rows)


@app.route("/appointments/<int:appointment_id>/delete", methods=["POST"])
def delete_appointment(appointment_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    flash(f"Запис №{appointment_id} видалено.", "success")
    return redirect(url_for("appointments"))


@app.route("/api/appointments")
def api_appointments():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT a.id, a.patient_name, a.phone, s.name AS service,
                   a.visit_date, a.comment, a.created_at
            FROM appointments a
            JOIN services s ON s.id = a.service_id
            ORDER BY a.id
        """)
        rows = cur.fetchall()
    for row in rows:
        row["visit_date"] = row["visit_date"].isoformat()
        row["created_at"] = row["created_at"].isoformat()
    return jsonify(rows)


@app.route("/api/services")
def api_services():
    return jsonify(fetch_services())


init_db()

if __name__ == "__main__":
    app.run(debug=True)
