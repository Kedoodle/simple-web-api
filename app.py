import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


@app.route("/health")
def health():
    return "healthy"


@app.route("/metadata")
def metadata():
    metadata = {
        "version": os.getenv("VERSION", "version not found"),
        "description": "a simple flask web api just for fun",
        "lastcommitsha": os.getenv("COMMIT_SHA", "last commit sha not found"),
    }
    return jsonify(metadata)
