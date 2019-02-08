import json
import os
import requests
from github import Github
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

def init_gh_user():
    return Github("hapd", "mAJORPROJECT19").get_user()

@app.route('/addNewUser', methods=['POST'])
def addNewUser():
    req = request.get_json(silent=True, force=True)
    db = init_gh_user().get_repo("database")
    users = db.get_contents("users.json")
    temp = users.decoded_content.decode("utf-8")
    temp = json.loads(temp)
    pid = temp["currentPID"]
    temp[str(pId)] = {
        "name": req.get('name'),
        "pin": req.get('pin'),
        "age": req.get('age'),
        "dob": req.get('dob'),
        "gender": req.get('gender')
    }
    temp["currentPID"] = int(temp["currentPID"])
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

@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    req = request.get_json(silent=True, force=True)
    db = init_gh_user().get_repo("database")
    users = db.get_contents("users.json")
    temp = users.decoded_content.decode("utf-8")
    temp = json.loads(temp)
    if(temp[req.get('pId')["pin"]] == req.get("pin")):
        res = {
            "Login Access": "True"
        }
    else:
        res = {
            "Login Access": "False"
        }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')