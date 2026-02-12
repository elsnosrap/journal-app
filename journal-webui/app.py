import os
import sqlite3
from flask import Flask, render_template_string, g

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", ".data", "data.db")

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Journal</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        h1 { border-bottom: 1px solid #ccc; padding-bottom: 10px; }
        ul { list-style: none; padding: 0; }
        li { padding: 8px 0; border-bottom: 1px solid #eee; }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Journal Entries</h1>
    {% if dates %}
    <ul>
        {% for date in dates %}
        <li><a href="/entry/{{ date }}">{{ date }}</a></li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No entries yet.</p>
    {% endif %}
</body>
</html>
"""

ENTRY_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Entry — {{ created }}</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        h1 { border-bottom: 1px solid #ccc; padding-bottom: 10px; }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .record { margin-bottom: 20px; }
        .label { font-weight: bold; color: #333; }
        .value { margin-top: 4px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <a href="/">&larr; Back</a>
    <h1>{{ created }}</h1>
    {% for record in records %}
    <div class="record">
        <div class="label">{{ record.label }}</div>
        <div class="value">{{ record.value }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    db = get_db()
    rows = db.execute(
        "SELECT DISTINCT created FROM user_data ORDER BY created DESC"
    ).fetchall()
    dates = [row["created"] for row in rows]
    return render_template_string(INDEX_TEMPLATE, dates=dates)


@app.route("/entry/<path:created>")
def entry(created):
    db = get_db()
    rows = db.execute(
        "SELECT u.key, u.int_value, u.text_value, d.label "
        "FROM user_data u JOIN data_types d ON u.data_type = d.key "
        "WHERE u.created = ? ORDER BY u.key",
        (created,),
    ).fetchall()
    records = []
    for row in rows:
        value = row["int_value"] if row["int_value"] is not None else row["text_value"]
        if value is not None:
            records.append({"label": row["label"], "value": value})
    return render_template_string(ENTRY_TEMPLATE, created=created, records=records)


if __name__ == "__main__":
    app.run(debug=True)
