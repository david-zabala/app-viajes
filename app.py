from flask import Flask, render_template, request, redirect, url_for
import scraper
import os
import pandas as pd

app = Flask(__name__)
CSV_FILE = "precios.csv"

@app.route("/", methods=["GET", "POST"])
def index():
    precio = None
    if request.method == "POST":
        origen = request.form["origen"].strip().upper()
        destino = request.form["destino"].strip().upper()
        salida = request.form["salida"]
        regreso = request.form["regreso"]
        precio = scraper.get_precio_kayak(origen, destino, salida, regreso)
        # redirect to historial to see saved entries
        return redirect(url_for("historial"))
    return render_template("index.html")

@app.route("/historial")
def historial():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            records = df.to_dict(orient="records")
        except Exception:
            records = []
    else:
        records = []
    return render_template("historial.html", datos=records)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
