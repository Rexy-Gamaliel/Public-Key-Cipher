from flask import *
import os

from ElGamal.elgamal import ElGamal

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/elgamal')
def elgamal():
    return render_template("elgamal.html")

@app.route('/elgamal/genkey')
def elgamal_genkey():
    gamal = ElGamal()
    gamal.key.generate()
    gamal.dumpKey()
    key = dict()
    key['y'], key['g'], key['p'] = gamal.key.public()
    key['x'], key['p'] = gamal.key.private()
    for k in key:
        key[k] = str(key[k])
    return key

if __name__ == "__main__":
    app.run(debug=True)