import flask
from score import score

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def flask_wrapper():
    return flask.jsonify(score.run(flask.request.json))

if __name__ == "__main__":
    score.init()
    app.run(host="0.0.0.0")