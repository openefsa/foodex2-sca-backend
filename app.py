from flask import Flask, request
from flask_cors import CORS


# init Flask and enable Cross Origin Resource Sharing
app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST'])
def getCode():
    # get the passed json file
    data = request.get_json()

    # if key doesnt exist return none
    baseterm = data['baseterm']
    # facets = data['facets']

    # concat result by comma
    result = ",".join(baseterm)

    return result


if __name__ == "__main__":
    app.run(debug=True)
