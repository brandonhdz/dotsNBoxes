from flask import *
from .appData import Data

app = Flask(__name__)
app.config['DEBUG'] = True

# The entire game state is accessed and updated via metaData
# initialized bellow as the Data class
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
    Used to be called by the front end via an AJAX call as an endpoint to render the grid.
    :return:JSON of the game state see appData.py for
    """
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

    The above is a request to run metaData.updateGridSize(5)
    The request is made within dotsNBoxes.js in the
    resizeMeta() method

    This route is abstracted for other calls and functionality
    app.py's metaData is of type Data()

    method: The Data function to be called
    delta: Data to be passed to delta
    :return: JSON of appData by redirection
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