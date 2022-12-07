"""Server for movie benevolence app."""

from flask import Flask

app = Flask(__name__)


# Replace this with routes and view functions!


if __name__ == "main":

    app.run(host="0.0.0.0", debug=True, port=5001)