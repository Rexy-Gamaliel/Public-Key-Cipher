from flask import *
import os
from constant import KEY_DIR

from elgamal import ElGamal
from paillier import Paillier

app = Flask(__name__)
app.secret_key = os.urandom(24)

TEMP_DIR = "./temp/"

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

@app.route('/elgamal/encrypt', methods=["POST", "GET"])
def elgamal_encrypt():
    data = json.loads(request.form.get('data'))
    gamal = ElGamal()
    gamal.key.setKey(int(data["p"]),\
                    int(data["g"]), \
                    int(data["x"]), \
                    int(data["y"]))
    open(TEMP_DIR+"input.txt", 'w').write(data["text"])
    gamal.encrypt_file(TEMP_DIR+"input.txt", \
                        TEMP_DIR+"output.txt")
    result = open(TEMP_DIR+"output.txt", 'r').read()
    return json.jsonify(result)

@app.route('/elgamal/decrypt', methods=["POST", "GET"])
def elgamal_decrypt():
    data = json.loads(request.form.get('data'))
    gamal = ElGamal()
    gamal.key.setKey(int(data["p"]),\
                    int(data["g"]), \
                    int(data["x"]), \
                    int(data["y"]))
    gamal.textbox_to_file(data["text"],\
                            TEMP_DIR+"input.txt")
    gamal.decrypt_file(TEMP_DIR+"input.txt", \
                        TEMP_DIR+"output.txt")
    result = open(TEMP_DIR+"output.txt", 'r').read()
    print(result)
    return result


@app.route("/paillier")
def paillier():
    return render_template("paillier.html")

@app.route("/paillier/genkey")
def paillier_genkey():
    pail = Paillier()
    pail.dumpKey(KEY_DIR+"paillier.pub",\
                KEY_DIR+"paillier.pri")
    key = dict()
    key['g'], key['n'] = pail.key.public()
    key['h'], key['u'] = pail.key.private()
    for k in key:
        key[k] = str(key[k])
    return key

@app.route("/paillier/encrypt", methods=["POST", "GET"])
def paillier_encrypt():
    data = json.loads(request.form.get('data'))
    pail = Paillier()
    pail.key.setKey(int(data["g"]), \
                    int(data["n"]), \
                    int(data["h"]), \
                    int(data["u"]))
    open(TEMP_DIR+"input.txt", 'w').write(data["text"])
    pail.encrypt_file(TEMP_DIR+"input.txt", \
                        TEMP_DIR+"output.txt")
    result = open(TEMP_DIR+"output.txt", 'r').read()
    return result

@app.route("/paillier/decrypt", methods=["POST", "GET"])
def paillier_decrypt():
    data = json.loads(request.form.get('data'))
    pail = Paillier()
    pail.key.setKey(int(data["g"]), \
                    int(data["n"]), \
                    int(data["h"]), \
                    int(data["u"]))
    open(TEMP_DIR+"input.txt", 'w').write(data["text"])
    pail.decrypt_file(TEMP_DIR+"input.txt", \
                        TEMP_DIR+"output.txt")
    result = open(TEMP_DIR+"output.txt", 'r').read()
    return result

if __name__ == "__main__":
    app.run(debug=True)