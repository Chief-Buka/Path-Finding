import random
from Nodes import *
from Settings import *
import time
from cmu_112_graphics import *

class Cell():
    def __init__(self, app, row, col):
        self.col = col
        self.row = row
        self.color = app.fill

class Wall():
    def __init__(self, row, col, state):
        self.row = row
        self.col = col
        self.state = state

    def __repr__(self):
        return(f'({self.row}, {self.col})')

def appStarted(app):
    app.cols = 10
    app.rows = 5
    app.filledCells = set()
    app.fill="black"
    app.bottomMargin = 100
    app.buttons = ["DFS", "BFS", "GBFS", "A*"]
    app.startNode = None
    app.goalState = None
    app.removedCell = False
    app.walls = []
    app.mazeWalls = []
    '''app.dir = [(-1,-1), (0, -1), (1, -1),
                (-1, 0), (0, 0), (1, 0),
                (-1, 1), (0, 1), (1, 1)]'''
    app.dir = [(0, -1), (-1, 0), (1, 0), (0, 1)]

def keyPressed(app, event):
    if event.key == 'b':
        app.fill = "blue"
    elif event.key == 'r':
        app.fill = "red"
    elif event.key == 'g':
        app.fill = "green"
    elif event.key == 'Enter':
        BFS(app)
    elif event.key == 's':
        app.filledCells = set()
    elif event.key == 'p':
        generateMaze(app)

def generateMaze(app):
    app.mazeWalls = []
    blocked = False
    passage = True
    for row in range(app.rows):
        for col in range(app.cols):
            wall = Wall(row, col, blocked)
            app.mazeWalls.append(wall)

    
    curr = random.choice(app.mazeWalls)
    curr.state = passage
    frontier = []
    for wall in app.mazeWalls:
        if (((((wall.row <= (curr.row-2)) or (wall.row <= (curr.row+2))) and wall.col == curr.col) or
            (((wall.col <= (curr.col-2)) or (wall.col <= (curr.col+2))) and wall.row == curr.row)) and
            (wall.state == blocked)):
            frontier.append(wall)
    while(len(frontier) > 0):
        neighbors = []
        curr = random.choice(frontier)
        for wall in app.mazeWalls:
            if (((((wall.row <= (curr.row-2)) or (wall.row <= (curr.row+2))) and wall.col == curr.col) or
                (((wall.col <= (curr.col-2)) or (wall.col <= (curr.col+2))) and wall.row == curr.row)) and
                (wall.state == blocked)):
                neighbors.append(wall)
        if len(neighbors) < 2:
            break
        print(f'neighbors: {neighbors}')
        print(f'frontier: {frontier}')
        neighbor = random.choice(neighbors)
        dx = int((neighbor.col - curr.col)/2)
        dy = int((neighbor.row - curr.row)/2)
        #print(dx,dy)
        newRow, newCol = curr.row+dy, curr.col+dx
        for wall in app.mazeWalls:
            if (wall.row == newRow and wall.col == newCol):
                wall.state = passage
                break
        frontier.extend(neighbors)
        frontier.remove(curr)
    
    for wall in app.mazeWalls:
        if wall.state == blocked:
            app.fill = "green"
            cell = Cell(app, wall.row, wall.col)
            app.walls.append((wall.row, wall.col))
            app.filledCells.add(cell)

def BFS(app):
        app.explored = set()
        app.exploredStates = set()
        frontier = Queue()
        frontier.add(app.startNode)

        while(not frontier.isEmpty()):
            # Remove node from frontier
            currNode = frontier.remove()

            # If current node is goal return path
            if(currNode.state == app.goalState):
                constructPath(app, currNode)
                return None
            else:
                # Add node to explored set
                app.explored.add(currNode)
                app.exploredStates.add(currNode.state)
                # Expand the node
                random.shuffle(app.dir)
                for direction in app.dir:
                    newCol = direction[1]+currNode.state[1]
                    newRow = direction[0]+currNode.state[0]
                    newState = (newRow, newCol)
                    if(((newRow >= 0) and (newRow < app.rows) and (newCol >= 0) and (newCol < app.cols)) and
                       (newState not in app.exploredStates) and (newState not in app.walls) and 
                       not(frontier.containsState(newState))):
                       app.fill = "black"
                       cell = Cell(app, newRow, newCol)
                       addNode = Node(newState, currNode.state, direction, cell)
                       frontier.add(addNode)
        return None

def constructPath(app, goalNode):
    app.path = []
    currNode = goalNode
    while(currNode.parent != None):
        app.path.append((currNode.state))
        for node in app.explored:
            if (node.state == currNode.parent):
                currNode = node
                break
    app.path.reverse()
    for row, col in app.path:
        if (row != app.goalState[0] or col != app.goalState[1]):
            app.fill = "black"
            cell = Cell(app, row, col)
            app.filledCells.add(cell)        

def mousePressed(app, event):
    app.removedCell = False
    row, col = getCell(app, event.x, event.y)


    if (row < app.rows and col < app.cols):
        # For Start Node
        if (app.fill == "red"):
            #if no start node assign one
            if (app.startNode == None):
                assignStartNode(app, row, col)
                #if click on start node remove it
            elif(row == app.startNode.cell.row and col == app.startNode.cell.col):
                removeCell(app, app.startNode.cell.row, app.startNode.cell.col)
                app.startNode = None
            else:
                #if click somewhere assign the start node there
                removeCell(app, app.startNode.cell.row, app.startNode.cell.col)
                app.startNode = None
                assignStartNode(app, row, col)
        # For Goal State
        elif (app.fill == "blue"):
            if app.goalState == None:
                app.goalState = row, col
                cell = Cell(app, row, col)
                app.filledCells.add(cell)
            elif (row == app.goalState[0] and app.goalState[1]):
                removeCell(app, row, col)
                app.goalState = None
            else:
                removeCell(app, app.goalState[0], app.goalState[1])
                app.goalState = None
                app.goalState = row, col
                cell = Cell(app, row, col)
                app.filledCells.add(cell)

        elif (app.fill == "green"):
            if ((row, col) in app.walls):
                app.walls.remove((row, col))
                removeCell(app, row, col)
            else:
                app.walls.append((row, col))
                cell = Cell(app, row, col)
                app.filledCells.add(cell)

        
        #for cells that arent red
        else:
            removeCell(app, row, col)
            if (not app.removedCell):
                cell = Cell(app, row, col)
                app.filledCells.add(cell)
         
def assignStartNode(app, row, col):
    cell = Cell(app, row, col)
    app.filledCells.add(cell)
    app.startNode = Node((row, col), None, None, cell)

def assignGoalNode(app, row, col):
    cell = Cell(app, row, col)
    app.filledCells.add(cell)
    app.goalNode = Node((row, col), None, None, cell)

def removeCell(app, removeRow, removeCol):
    for cell in app.filledCells:
        if (cell.row == removeRow and cell.col == removeCol):
            app.filledCells.remove(cell)
            app.removedCell = True
            break

def getCell(app, x, y):
    gridWidth = app.width
    gridHeight = app.height-app.bottomMargin
    cellWidth = gridWidth/app.cols
    cellHeight = gridHeight/app.rows
    row = y//cellHeight
    col = x//cellWidth
    return row, col

def getCellBounds(app, row, col):
    gridWidth = app.width
    gridHeight = app.height-app.bottomMargin
    cellWidth = gridWidth/app.cols
    cellHeight = gridHeight/app.rows
    x0 = col*cellWidth
    x1 = (col+1)*cellWidth
    y0 = row*cellHeight
    y1 = (row+1)*cellHeight
    return (x0, y0, x1, y1)

def drawGrid(app, canvas):
    gridWidth = app.width
    gridHeight = app.height-app.bottomMargin
    cellWidth = gridWidth/app.cols
    cellHeight = gridHeight/app.rows

    for row in range(app.rows+1):
        canvas.create_line(0, cellHeight*row, app.width, cellHeight*row)
    for col in range(app.cols):
        canvas.create_line(cellWidth*col, 0, cellWidth*col, gridHeight)

def drawButtons(app, canvas):
    gridHeight = app.height-app.bottomMargin
    buttonWidth = int(app.width/4)
    for i in range(4):
        canvas.create_line(i*buttonWidth, gridHeight, i*buttonWidth, app.height)

    cx = buttonWidth/2
    cy = 0.5*(app.height-gridHeight)+gridHeight
    for button in app.buttons:
        canvas.create_text(cx, cy, text=button, font=f'Arial {int(buttonWidth/10)} bold')
        cx += buttonWidth

def fillCells(app, canvas):
    for cell in app.filledCells:
        x0, y0, x1, y1 = getCellBounds(app, cell.row, cell.col)
        canvas.create_rectangle(x0, y0, x1, y1, fill=cell.color)

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    fillCells(app, canvas)
    drawButtons(app, canvas)

runApp(width=1500, height=800)