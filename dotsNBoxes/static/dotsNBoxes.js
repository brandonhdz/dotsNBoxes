var ajax = document.createElement('script');

//Global input from form
var boardSize = null;

//App meta data from server
//TODO possible memory optimization?
var metaData = null; //JSON object
var tileScale = null; //Integer

var isValidRequest = null

//All line objects will be pushed here while
let lines = []

ajax.src = '//ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js';
document.getElementsByTagName('head')[0].appendChild(ajax);

function requestRender(){
    //retrieve board size from input
    boardSize = parseInt(document.getElementById("selSize").value);

    var restartGame = true
    //If game is in session
    if (metaData != null){
        restartGame = confirm("Game is currently in session\nStart new game?");
    }

    if (restartGame == true){
        //Resize the python app data
        resizeMeta(boardSize);
    }
}

//May be obsolete since resizeMeta is directly
//rerouted to /appData
function requestBoardData(){
    //Retrieve board meta data
    //Works asynchronously so call first
    $.getJSON({
        dataType: "json",
        type: "GET",
        url: "/appData",
        success: function (result) {
            metaData = result;
            tileScale = metaData.session.scale
            finishRender();
        }
    });
}

function resizeMeta(newSize){
    $.ajax({
        type : "GET",
        url : "/appData/lambda?method=updateGridSize&delta=" + newSize ,
        dataType: "json",
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            metaData = result;
            tileScale = metaData.session.scale;
            finishRender();
            }
	});
}

function finishRender(){
    //Make game_area visible
    document.getElementById('game_area').style.display = 'block';

    //Display current board size
    var board_header = document.getElementById('display_size');
    board_header.innerHTML = 'Board size: ' + boardSize;

    //Resize grid
    metaData.session.inSession = true;
    //This method calls draw
    resizeCanvas(boardSize*tileScale, boardSize*tileScale);
}

function setup() {
    myGrid = createCanvas(0,0);
    myGrid.parent("grid_area");
}

function draw() {
    //Keep this to maintain low CPU usage
    noLoop();
    background(253, 235, 208);
    if (metaData != null && metaData.session.size == boardSize){
        drawGrid();
    }
}

function mousePressed(){
    mX = mouseX;
    mY = mouseY;
    if (metaData != null && metaData.session.turn === 'player' && isWithinRange(mX, mY)){
        requestLine(mX, mY);

    }
}

function drawGrid() {
    if (metaData != null){
        //Set text size
        textSize(25);

        for(row = 0; row < boardSize; row++){
            for(column = 0; column < boardSize; column++){
                initEdge = metaData.tiles[row][column].edges[0];
                bottomEdge = metaData.tiles[row][column].edges[2];

                //Draw point
                stroke(0);
                strokeWeight(10);
                point(initEdge[0][0], initEdge[0][1]);
                if(row == boardSize-1){
                    point(bottomEdge[1][0], bottomEdge[1][1]);
                    if(column == boardSize-1){
                        point(bottomEdge[0][0], bottomEdge[0][1]);
                        point(initEdge[1][0], initEdge[1][1]);
                    }
                }
                else if(column == boardSize-1){
                    point(initEdge[1][0], initEdge[1][1]);
                }
                //Draw text
                strokeWeight(0);
                tileVal = metaData.tiles[row][column].value;
                text(tileVal, initEdge[0][0] + (tileScale/2), initEdge[0][1] + (tileScale/2));

                for(edgeIndex = 0; edgeIndex < 4; edgeIndex++){
                    drawingContext.setLineDash([]);
                    edge = metaData.tiles[column][row].edges[edgeIndex];
                    switch(edge[2]){
                        case "ai":
                            stroke(255, 0, 0);
                            break;

                        case "player":
                            stroke(0, 0, 255);
                            break;

                        default:
                            drawingContext.setLineDash([5,5]);
                            stroke(170);
                            break;
                    }
                    //Draw line
                    strokeWeight(4);
                    line(edge[0][0], edge[0][1], edge[1][0], edge[1][1]);
                }
                /*
                if (row < boardSize){
                    stroke(170);
                    strokeWeight(4);

                    //Draw across
                    lines.push(line(x*tileScale,y*tileScale, (x+1)*tileScale, y*tileScale));

                    //Render random calculated values for conquerable tiles
                    if (y < boardSize && x < boardSize){
                        strokeWeight(0);
                        text(metaData.tiles[y][x].value, (x*tileScale) + (tileScale/2), (y*tileScale) + (tileScale/2));
                    }
                }
                //Draw down
                stroke(170);
                strokeWeight(4);
                lines.push(line(x*tileScale,y*tileScale, (x)*tileScale,(y+1)*tileScale));

                stroke(0);
                strokeWeight(10);
                //Draw each point
                point(x*tileScale,y*tileScale);
                */
            }
        }
    }
}

function requestLine(mX, mY){
    var coordinate = [mX, mY];
    $.ajax({
        type : "GET",
        url : "/appData/lambda?method=requestEdge&delta=" + coordinate,
        dataType: "json",
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            isValidRequest = result;
            //Update the board data
            if (isValidRequest){
                metaData = requestBoardData();
            }
            else{
                alert("Invalid!\nPlease click on a free edge.");
            }
        }
    });
}

function fillLine(mX, mY){
    //this is to be called after the route call
}

function isWithinRange(mX, mY){
    brdPxlLength = tileScale * boardSize;
    let clickRange = 7;
    if (mX > -clickRange && mX < brdPxlLength + clickRange && mY > -clickRange && mY < brdPxlLength + clickRange){
        return true
    }
    return false
}