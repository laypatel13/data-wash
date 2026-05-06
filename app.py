import os
from flask import Flask, render_template, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "datawash-dev-key")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)