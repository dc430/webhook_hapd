import json
import os
import requests
from github import Github
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    gh = Github("hapd", "mAJORPROJECT19")
    u = gh.get_user()
    repo = u.get_repo("database")
    db = repo.get_file_contents("users.json")
    temp = db.decoded_content.decode("utf-8")
    emp = json.loads(temp)
    pid = temp["currentPID"]
    temp[str(pid)] = {
        "name": req.get('name'),
        "pin": req.get('pin'),
        "age": req.get('age'),
        "dob": req.get('dob'),
        "gender": req.get('gender')
    }
    temp["currentPID"] = int(temp["currentPID"])
    temp = json.dumps(temp, indent=4)
    try:
        db.update_file(db.path, "Update users", str(temp), db.sha)
        speech = "Account creation successful"
    except:
        speech = "Account creation failed"
    return {
    "fulfillmentText": speech,
    "source": "webhook-hapd-api"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















