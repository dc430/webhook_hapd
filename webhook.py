import json
import os
import requests
from github import Github
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

USER = "hapd"
PWD = "mAJORPROJECT19"

@app.route('/addUser', methods=['POST'])
def addUser():
    req = request.get_json(silent=True, force=True)
    gh = Github(USER, PWD)
    db = gh.get_repo("database")
    users = db.get_contents("users.json")
    temp = (users.decoded_content).decode("utf-8")
    temp = json.loads(temp)
    pid = temp["currentPID"]
    temp[str(pid)] = {
        "name": req.get('name'),
        "pin": req.get('pin'),
        "age": req.get('age'),
        "dob": req.get('dob'),
        "gender": req.get('gender')
    }
    temp["currentPID"] = str(int(temp["currentPID"])+1)
    temp = json.dumps(temp, indent=4)
    try:
        db.update_file(users.path, "Update users", str(temp), users.sha)
        s = 1
    except:
        s = 0
    if(s == 0):
        res = {
            "fullfillmentText": "New account creation failed"
        }
    else:
        res = {
            "fullfillmentText": "New account creation successful"
        }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')