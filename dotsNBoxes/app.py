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

@app.route("/appData/lambda")
def requestLambda():
    """
    Generic route that calls an internal method
    Usage:
    http://127.0.0.1:5000/appData/lambda?method=updateGridSize&delta=5

    method: The Data function to be called
    delta: Data to be passed to delta
    :return: json of appData
    """
    method = request.args.get('method')
    delta = request.args.get('delta')

    if method == 'updateGridSize' and delta is not None:
        method = getattr(metaData, method)
        method(delta)
        return redirect("/appData", code=302)

    elif method == 'requestEdge' and delta is not None:
        coordinate = delta.split(',')
        coordinate[0] = float(coordinate[0])
        coordinate[1] = float(coordinate[1])
        method = getattr(metaData, method)
        edgeAvailable = method(coordinate)
        if edgeAvailable:
            return "true"
        return "false"
    else:
        return redirect("/appData", code=405)