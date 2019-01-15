from flask import Flask
import http.client

app = Flask(__name__)

@app.route("/abc")
def helloabc():
    conn = http.client.HTTPConnection("backend:1234")
    conn.request('GET', '/abc')
    data = conn.getresponse().read()
    conn.close()
    return data

@app.route("/def")
def hellodef():
    conn = http.client.HTTPConnection('backend:1234')
    conn.request('GET', '/def')
    data = conn.getresponse().read()
    conn.close()
    return data
    

app.run(host='0.0.0.0', port=7000)
