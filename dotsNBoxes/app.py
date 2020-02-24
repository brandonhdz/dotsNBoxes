from flask import *
from .appData import Data

app = Flask(__name__)
app.config['DEBUG'] = True

metaData = None

@app.route("/")
@app.route("/index")
def index():
    global metaData
    # Initialize here for when refreshed
    metaData = Data()
    return render_template('index.html', AIScore=metaData.AIScore,
                           playerScore=metaData.playerScore)


@app.route("/appData")
def getAppData():
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
    Usage:
    http://127.0.0.1:5000/appData/update<updateGridSize>/<5>

    :param delta: The Data function to be called
    :param newData: Data to be passed to delta
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
    :return:
    """
    coordinate = (coordinate[1:-1]).split(',')
    coordinate[0] = float(coordinate[0])
    coordinate[1] = float(coordinate[1])
    edgeAvailable = metaData.requestEdge(coordinate)
    # TODO remove this variable FOR TESTING
    if edgeAvailable:
        return "true"
    return "false"
