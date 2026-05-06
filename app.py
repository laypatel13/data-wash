import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "datawash-dev-key")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        flash("No file part found.", "danger")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only CSV files are allowed.", "danger")
        return redirect(url_for("index"))

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    session["filepath"] = filepath
    session["original_name"] = file.filename

    return redirect(url_for("preview"))


@app.route("/preview")
def preview():
    filepath = session.get("filepath")
    if not filepath or not os.path.exists(filepath):
        flash("Session expired. Please upload again.", "warning")
        return redirect(url_for("index"))

    df = pd.read_csv(filepath)

    preview_html = df.head(20).to_html(
        classes="table table-dark table-bordered table-hover table-sm",
        index=True,
        border=0,
        na_rep="NaN"
    )

    stats = {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "filename": session.get("original_name"),
    }

    return render_template("preview.html", table=preview_html, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)