from flask import *
from .appData import Data

app = Flask(__name__)
app.config['DEBUG'] = True

metaData = None

@app.route("/")
@app.route("/index")
def index():
    """
    This is the home page of the webApp.
    metaData is an instance of appData which
    holds all the data, logic and state about the app

    see grid.py to view what is being generated
    :return: HTML template with initial variables
    """
    global metaData
    # Initialize here for when refreshed
    metaData = Data()
    return render_template('index.html', AIScore=metaData.AIScore,
                           playerScore=metaData.playerScore)


@app.route("/appData")
def getAppData():
    """
    Returns a JSON of the app metaData for the front end to render the grid
    :return: JSON of app data
    """
    return jsonify({'session': {'inSession': metaData.inSession,
                                'turn': metaData.currentTurn,
                                'scale': metaData.getScale(),
                                'size': metaData.getGridSize(),
                                'score': {'ai': metaData.AIScore,
                                          'player': metaData.playerScore}},
                    'tiles': metaData.jsonifyTiles()})

@app.route("/appData/lambda<delta>", defaults={"newData": None})
@app.route("/appData/lambda<delta>/<newData>")
def requestLambda(delta, newData):
    """
    Usage eg:
    http://127.0.0.1:5000/appData/update<updateGridSize>/<5>

    The above is a request to run appData.updateGridSize(5)
    The request is made within dotsNBoxes.js in the
    resizeMeta() method

    This route is abstracted for other calls and functionality
    app.py has instance of appData as metaData

    :param delta: The appData function to be called
    :param newData: appData to be passed to delta
    :return: json of appData
    """
    delta = getattr(metaData, delta[1:-1])
    if newData is not None:
        delta(newData[1:-1])
    else:
        delta()
    return redirect("/appData", code=302)

@app.route("/appData/requestLine<coordinate>")
def requestLine(coordinate):
    """
    Checks if the coordinate given is within a valid line
    :param coordinate: The requested point to see if
    there exists an available line
    :return: "true" | "false"
    """
    coordinate = (coordinate[1:-1]).split(',')
    coordinate[0] = float(coordinate[0])
    coordinate[1] = float(coordinate[1])
    edgeAvailable = metaData.requestEdge(coordinate)
    # TODO remove this variable FOR TESTING
    if edgeAvailable:
        return "true"
    return "false"
