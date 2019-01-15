from flask import Flask
app = Flask(__name__)

@app.route("/abc")
def helloabc():
    return "Hello World! abc This is remote\n"

@app.route("/def")
def hellodef():
    return "Hello World! def This is remote\n"

app.run(host='0.0.0.0', port=6000)
