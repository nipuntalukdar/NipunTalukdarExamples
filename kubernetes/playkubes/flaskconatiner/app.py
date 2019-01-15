from flask import Flask
import http.client

app = Flask(__name__)

@app.route("/abc")
def helloabc():
    conn = http.client.HTTPConnection("192.168.13.129:6000")
    conn.request('GET', '/abc')
    data = conn.getresponse().read()
    conn.close()
    return data

@app.route("/def")
def hellodef():
    conn = http.client.HTTPConnection('192.168.13.129:6000')
    conn.request('GET', '/def')
    data = conn.getresponse().read()
    conn.close()
    return data
    

app.run(host='0.0.0.0', port=5000)
