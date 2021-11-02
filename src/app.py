from flask import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/elgamal')
def elgamal():
    return render_template("elgamal.html")


if __name__ == "__main__":
    app.run(debug=True)