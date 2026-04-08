from flask import Flask, render_template, request
from main import scrape_amazon

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    data = None

    if request.method == "POST":
        url = request.form.get("url")

        if url:
            try:
                data = scrape_amazon(url)
            except Exception as e:
                print("ERROR:", e)
                data = None

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)