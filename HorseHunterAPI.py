import random

from flask import Flask, Response, request
from getLines import VALID_LEVEL, VALID_TARGET, getLines

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    config = {
        "level": "max",
        "target": "female"
    }
    level = request.args.get("level")
    target = request.args.get("target")

    if level in VALID_LEVEL:
        config["level"] = level
    if target in VALID_TARGET:
        config["target"] = target

    lines = getLines(config)

    return Response(random.choice(lines))

if __name__ == "__main__":
    app.run(port=6675)