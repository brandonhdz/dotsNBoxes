# dotsNBoxes

*IN DEVELOPMENT*

A recreation of the game Dots N Boxes. Game concept can be read [here](https://en.wikipedia.org/wiki/Dots_and_Boxes).
## Getting Started

### Technologies
The following technologies are used to run the Web App:
* [P5.js](https://p5js.org/) to render the grid
* [AJAX](https://api.jquery.com/category/ajax/) to retrieve game state data 
* [Flask Framework](https://flask.palletsprojects.com/en/1.1.x/) for creating routes and managing communication between
the Back-End and Front-End

### Prerequisites
* python-3.6.0 or later

### Installing
The following is set up within the Windows Terminal:

`>git clone https://github.com/brandonhdz/softwareProjects.git`
1) Set up venv
2) Install Python modules:
    
    `>pip install -r "requirements.txt"`
3) Set up environment variables:
     ```
      >set FLASK_APP=run.py
      >set FLASK_ENV=development
      ```
    *Skip FLASK_ENV to disable debugging*

### Running Locally
```>flask run```

Expected Output:

```
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

On your preferred browser view the web app locally (Chrome is recommended): 

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

*See [app.py](https://github.com/brandonhdz/dotsNBoxes/blob/dev/dotsNBoxes/app.py)
to view the routes and use cases*

In the root page the user is prompted to to select a grid size to initialize the game

### Game State
To view the current game state data open another tab and navigate to:

[http://127.0.0.1:5000/appData](http://127.0.0.1:5000/appData)

The route is activated by the `getAppData()` method within
[app.py](https://github.com/brandonhdz/dotsNBoxes/blob/dev/dotsNBoxes/app.py)
which is used as a JSON endpoint for the current game state.

Furthermore, note the Get method when the grid is initialized:

`127.0.0.1 - - [30/Mar/2020 23:22:12] "?[32mGET /appData/lambda?method=updateGridSize&delta=2 HTTP/1.1?[0m" 302 -`

See `resizeMeta()` under 
[dotsNBoxes.js](https://github.com/brandonhdz/dotsNBoxes/blob/dev/dotsNBoxes/static/dotsNBoxes.js).
It calls a the `lambdaRequest()` route which is queried within the `resizeMeta(newSize)` function:

`url : "/appData/lambda?method=updateGridSize&delta=" + newSize ,`

The above is query computationally equivalent to:
```python
# See app.py
# metaData is a Data() object which holds the entire game state
# which can be accessed and updated 

metaData.updateGridSize(newSize)
```

### AI Functionality

The computer is optimizes the next turn by utilizing the MiniMax algorithm

See [heuristic.py](https://github.com/brandonhdz/dotsNBoxes/blob/dev/dotsNBoxes/heuristic.py)
*(IN DEVELOPMENT)*

### Looking Forward

* Finish AI Functionality
* Memory Optimization
* Proper Grid Render
* Refactoring