from datetime import datetime
import sqlite3
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "notes.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-notes-manager-secret-key"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )


def now_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_note(note_id):
    return get_db().execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()


def validate_title(title):
    if not title or not title.strip():
        return "Title is required and cannot be empty."
    return None


@app.route("/")
def index():
    notes = (
        get_db()
        .execute("SELECT * FROM notes ORDER BY updated_at DESC, created_at DESC")
        .fetchall()
    )
    return render_template("index.html", notes=notes)


@app.route("/notes", methods=["POST"])
def create_note():
    title = request.form.get("title", "")
    content = request.form.get("content", "")
    error = validate_title(title)

    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    timestamp = now_timestamp()
    get_db().execute(
        """
        INSERT INTO notes (title, content, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """,
        (title.strip(), content.strip(), timestamp, timestamp),
    )
    get_db().commit()
    flash("Note created successfully.", "success")
    return redirect(url_for("index"))


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    note = get_note(note_id)
    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        error = validate_title(title)

        if error:
            flash(error, "error")
            return render_template("edit.html", note=note, title=title, content=content)

        get_db().execute(
            """
            UPDATE notes
            SET title = ?, content = ?, updated_at = ?
            WHERE id = ?
            """,
            (title.strip(), content.strip(), now_timestamp(), note_id),
        )
        get_db().commit()
        flash("Note updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", note=note, title=note["title"], content=note["content"])


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    note = get_note(note_id)
    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("index"))

    get_db().execute("DELETE FROM notes WHERE id = ?", (note_id,))
    get_db().commit()
    flash("Note deleted successfully.", "success")
    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
