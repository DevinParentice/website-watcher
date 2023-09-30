from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from watcher import main

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=["GET", "POST", "DELETE"])


@app.route("/api/getMonitors")
def get_monitors():
    with open("config.json") as f:
        saved_content = json.load(f)
    return jsonify(saved_content)


@app.route("/api/addWebsite", methods=["POST"])
def add_website():
    try:
        with open("config.json") as f:
            saved_config = json.load(f)
        saved_config["websites"].append(request.get_json())
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(saved_config, f, ensure_ascii=False)
    except Exception as e:
        return {"success": False, "error": e}
    return {"success": True, "error": None}


@app.route("/api/deleteWebsite", methods=["DELETE"])
def delete_website():
    try:
        request_json = request.get_json()
        with open("config.json") as f:
            saved_config = json.load(f)
        for i, website in enumerate(saved_config["websites"]):
            if website["name"] == request_json["name"]:
                del saved_config["websites"][i]
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(saved_config, f, ensure_ascii=False)
    except Exception as e:
        return {"success": False, "error": e}
    return {"success": True, "error": None}


@app.route("/api/addElement", methods=["POST"])
def add_element():
    with open("config.json") as f:
        saved_config = json.load(f)
    for website in saved_config["websites"]:
        if website["name"] == request.get_json()["name"]:
            website["elements"].append[request.get_json()["element"]]
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(saved_config, f, ensure_ascii=False)
    return "", 204


@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    with open("config.json") as f:
        saved_config = json.load(f)
    saved_config["websites"].append(request.get_json())
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(saved_config, f, ensure_ascii=False)
    return "", 204


app.run(debug=True)
