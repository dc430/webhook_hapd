import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    pId = req.get('patientID')
    with open('User.json', 'r') as f: 
        d = json.load(f)
    d[str(pId)] = {
        "name": req.get('name'),
        "pin": req.get('pin'),
        "age": req.get('age'),
        "dob": req.get('dob'),
        "gender": req.get('gender')
    }
    with open('User.json', 'w') as f: 
        json.dump(d, f, indent=4)
    return {
    "fulfillmentText": d,
    "source": "webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')