from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from .database import get_db, init_db, close_db

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__)
app.config["DATABASE"] = BASE_DIR / "database" / "assets.db"

with app.app_context():
    init_db()

app.teardown_appcontext(close_db)

def calculate_criticality(confidentiality, integrity, availability):
    score = round((confidentiality + integrity + availability) / 3, 2)
    if score >= 4:
        level = "Critical"
    elif score >= 3:
        level = "High"
    elif score >= 2:
        level = "Medium"
    else:
        level = "Low"
    return score, level

@app.route("/")
def dashboard():
    assets = get_db().execute("SELECT * FROM assets ORDER BY id DESC").fetchall()
    return render_template("dashboard.html", assets=assets)

@app.route("/assets")
def asset_inventory():
    assets = get_db().execute("SELECT * FROM assets ORDER BY id DESC").fetchall()
    return render_template("assets.html", assets=assets)

@app.route("/assets/add", methods=["GET", "POST"])
def add_asset():
    if request.method == "POST":
        name = request.form["name"].strip()
        asset_type = request.form["asset_type"]
        owner = request.form["owner"].strip()
        description = request.form.get("description", "").strip()
        c = int(request.form["confidentiality"])
        i = int(request.form["integrity"])
        a = int(request.form["availability"])
        score, level = calculate_criticality(c, i, a)

        db = get_db()
        db.execute(
            """INSERT INTO assets
            (name, asset_type, owner, description, confidentiality,
             integrity, availability, criticality_score, criticality)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, asset_type, owner, description, c, i, a, score, level)
        )
        db.commit()
        return redirect(url_for("asset_inventory"))
    return render_template("add_asset.html")

if __name__ == "__main__":
    app.run(debug=True)
