# A* TODO
# walls TODO

import pygame as pg
from pygame import color
import random
import math
import queue
from Settings import *

class Game():

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.tile_size = 20
        self.tilesInButton = 10
        self.posToTile = dict() # map (row, col) to tile
        self.changeWeights = False
        self.eraser = False
        self.sliderOn = False
        self.labels = {0:'Breathe-First', 2:'Depth-First', 4:'Iterative Deepening', 6:'Grredy Best-First', 8:'A*', 10:'RESET(Just Search)', 12:'RESET ALL', 14: 'Wall/Weight', 16:'Eraser'}
        '''self.directions = [(-1, 1),  (0, 1), (1, 1),
                           (-1, 0),  (0, 0), (1, 0),
                           (-1, -1), (0, -1), (1, -1)]'''
        self.directions = [          (0, 1),
                           (-1, 0),  (0, 0), (1, 0),
                                     (0, -1)        ]
        self.buttonDown = False
        
    def new(self):
        # Start a new game
        self.allTiles = pg.sprite.Group()
        self.buttons = pg.sprite.Group()

        # Create all of tiles in a grid 
        #GUI
        for i in range(WIDTH//self.tile_size-self.tilesInButton):
            for j in range(HEIGHT//self.tile_size):
                tile = Tile(i*self.tile_size, j*self.tile_size, self)
                self.posToTile[(i, j)] = tile # creates map to (row, col) to tile
                self.allTiles.add(tile)

        
        # Draw buttons
        for i in self.labels:
            button  = Button(WIDTH-self.tilesInButton*self.tile_size, i*10, self, self.labels[i])
            self.buttons.add(button)
        self.buttonHeight = button.buttonHeight
        self.buttonWidth = button.buttonWidth

        # Slider
        self.slider = Slider(WIDTH-self.tilesInButton*self.tile_size, 9*self.buttonHeight, self)
            
        
        


        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.allTiles.update()
        

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.MOUSEBUTTONUP:
                self.buttonDown = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.buttonDown = True
                pressed = pg.mouse.get_pressed()
                pos = pg.mouse.get_pos()
                # SEARCHES
                if ((pos[0] > WIDTH - self.buttonWidth) and (pos[0] < WIDTH) and (pos[1] > 0) and (pos[1] < self.buttonHeight) and pressed == (1,0,0)):
                    print('BFS')
                    self.BFS((20,20), (30, 10))
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > self.buttonHeight and pos[1] < 2*self.buttonHeight) and pressed == (1,0,0)):
                    print('DFS')
                    self.DFS((20,20), (30, 30))
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 2*self.buttonHeight and pos[1] < 3*self.buttonHeight) and pressed == (1,0,0)):
                    print('IterativeDFS')
                    self.IterativeDFS((20,20), (27, 27))
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 3*self.buttonHeight and pos[1] < 4*self.buttonHeight) and pressed == (1,0,0)):
                    print('Greedy Search')
                    self.GreedySearch((20,20), (40, 10))
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 4*self.buttonHeight and pos[1] < 5*self.buttonHeight) and pressed == (1,0,0)):
                    print('A* Search')
                    self.Astar((20,20), (40, 10))
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 5*self.buttonHeight and pos[1] < 6*self.buttonHeight) and pressed == (1,0,0)):
                    print('Reset Search')
                    self.reset(clearWalls=False)
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 6*self.buttonHeight and pos[1] < 7*self.buttonHeight) and pressed == (1,0,0)):
                    print('Reset')
                    self.reset()
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 7*self.buttonHeight and pos[1] < 8*self.buttonHeight) and pressed == (1,0,0)):
                    print('Weight Switch')
                    self.eraser = False
                    self.changeWeights =  not self.changeWeights
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 8*self.buttonHeight and pos[1] < 9*self.buttonHeight) and pressed == (1,0,0)):
                    print('Eraser')
                    self.changeWeights = False
                    self.eraser =  not self.eraser
                if ((pos[0] > WIDTH - self.buttonWidth and pos[0] < WIDTH and pos[1] > 9*self.buttonHeight and pos[1] < 10*self.buttonHeight) and pressed == (1,0,0)):
                    print('Slider')
                    self.changeWeights = False
                    self.eraser = False
                    self.sliderOn = True
                else:
                    self.sliderOn = False


                
                    


            #tile weights
            if self.buttonDown and self.changeWeights:
                # WALLS
                pos = pg.mouse.get_pos()
                x = pos[0]//self.tile_size
                y = pos[1]//self.tile_size
                if x < WIDTH//self.tile_size-self.tilesInButton and y//self.tile_size < HEIGHT//self.tile_size:
                    tile = self.posToTile[(x, y)]
                    tile.Weight = (self.slider.by +(self.slider.bx-1250))//20
                    print(tile.Weight, ((self.slider.by +(self.slider.bx-1250)))//20)
            elif self.buttonDown and self.eraser:
                # Eraser
                pos = pg.mouse.get_pos()
                x = pos[0]//self.tile_size
                y = pos[1]//self.tile_size
                if x < WIDTH//self.tile_size-self.tilesInButton and y//self.tile_size < HEIGHT//self.tile_size:
                    tile = self.posToTile[(x, y)]
                    tile.Weight = 1
                    tile.isWall = False
            elif self.buttonDown and self.sliderOn:
                # Weight Slider
                self.slider.update()
            elif self.buttonDown:
                # WALLS
                pos = pg.mouse.get_pos()
                x = pos[0]//self.tile_size
                y = pos[1]//self.tile_size
                if x < WIDTH//self.tile_size-self.tilesInButton and y//self.tile_size < HEIGHT//self.tile_size:
                    tile = self.posToTile[(x, y)]
                    tile.isWall = True
            
            
                


    def draw(self):
        # Game Loop - Draw
        self.screen.fill(WHITE)
        self.allTiles.draw(self.screen)
        for button in self.buttons:
            button.draw()
        self.slider.draw()

        # Draw the lines to separate the tiles
        self.drawGrid()

        pg.display.flip()

    def drawGrid(self):
        #GUI
        for col in range(WIDTH//self.tile_size-self.tilesInButton+1):
            pg.draw.line(self.screen, BLACK, (col*self.tile_size, 0), (col*self.tile_size, HEIGHT), 1)
        for row in range(HEIGHT//self.tile_size):
            #GUI
            pg.draw.line(self.screen, BLACK, (0, row*self.tile_size), (WIDTH, row*self.tile_size), 1)

    def inBounds(self, position):
        #GUI
        return ((position[0] < WIDTH//self.tile_size-self.tilesInButton and position[0] >= 0) and
                (position[1] < HEIGHT//self.tile_size and position[1] >= 0))

    def reconstructPath(self, last):
        curr = last
        while(curr.prev != None):
            tile = self.posToTile[curr.pos]
            tile.inPath = True
            tile.update()
            tile.draw()

            curr = curr.prev
        return

    def BFS(self, start, end):
        visitedSet = set()
        discovered = queue.Queue() # holds Position objects(row, col, prev) for tile

        discovered.put(Position(start[0], start[1]))
        while( not discovered.empty()):
            # Get a Postion obj from known positions
            curr = discovered.get()
            
            if (not (curr.pos in visitedSet)):
                # Get the actual tile using the map
                tile = self.posToTile[curr.pos]
                tile.visited = True

                if (curr.pos == start):
                    tile.isStart = True
                # Goal check
                if (curr.pos == end):
                    tile.isEnd = True
                    self.reconstructPath(curr)
                    return

                # So the search is animated as it is happening
                tile.update()
                tile.draw()
                #pg.time.delay(100)

                visitedSet.add(curr.pos)
                # Look at the neighbors
                random.shuffle(self.directions)
                for direction in self.directions:
                    position = Position(curr.x+direction[0], curr.y+direction[1], curr)
                    if (not(position.pos in visitedSet) and self.inBounds(position.pos) and (not self.posToTile[position.pos].isWall)):
                        discovered.put(position)
                        self.posToTile[position.pos].wasDiscovered = True
                        self.posToTile[position.pos].update()
                        self.posToTile[position.pos].draw()
                

                        
        return

    def DFS(self, start, end, maxDepth=math.inf):
        visitedSet = set()
        discovered = queue.LifoQueue() # holds Position objects(row, col, prev) for tile
        discovered.put(Position(start[0], start[1], depth=0))

        while( not discovered.empty()):
            
            # Get a Postion obj from known positions
            curr = discovered.get()

            if (not (curr.pos in visitedSet) and curr.depth < maxDepth):

                # Get the actual tile using the map
                tile = self.posToTile[curr.pos]
                tile.visited = True

                if (curr.pos == start):
                    tile.isStart = True
                # Goal check
                if (curr.pos == end):
                    tile.isEnd = True
                    self.reconstructPath(curr)
                    return True

                # So the search is animated as it is happening
                tile.update()
                tile.draw()
                #pg.time.delay(100)

                visitedSet.add(curr.pos)
                # Look at the neighbors
                #self.directions.reverse()
                random.shuffle(self.directions)
                for direction in self.directions:
                    x = curr.x+direction[0] # next postiion x
                    y = curr.y+direction[1] # next position y
                    nextDepth = math.floor(math.sqrt((x-start[0])**2 + (y-start[0])**2)) # Euclidian distance from start position
                    position = Position(x, y, prev=curr, depth=nextDepth)
                    if (not(position.pos in visitedSet) and self.inBounds(position.pos) and (not self.posToTile[position.pos].isWall)):
                        discovered.put(position)
                        self.posToTile[position.pos].wasDiscovered = True
                        self.posToTile[position.pos].update()
                        self.posToTile[position.pos].draw()
                        
        return False

    def IterativeDFS(self, start, end):
        found = False
        maxDepth = 0
        while (not found):
            self.reset(clearWalls=False)
            found = self.DFS(start, end, maxDepth)
            maxDepth+=1
            pg.time.delay(100)

    def GreedySearch(self, start, end):
        visitedSet = set()
        discovered = [] # holds Position objects(row, col, prev) for tile

        first = Position(start[0], start[1])
        discovered.append((first, 0))
        while(len(discovered) > 0):
            # Get the position from  known positions with smallest manhattan distance to goal(end)
            minDistance = math.inf
            for position, distance in discovered:
                if (distance < minDistance):
                    curr = position
                    minDistance = distance
                    
            discovered.remove((curr, minDistance))
            
            if (not (curr.pos in visitedSet)):
                # Get the actual tile using the map
                tile = self.posToTile[curr.pos]
                tile.visited = True

                if (curr.pos == start):
                    tile.isStart = True
                # Goal check
                if (curr.pos == end):
                    tile.isEnd = True
                    self.reconstructPath(curr)
                    return

                # So the search is animated as it is happening
                tile.update()
                tile.draw()
                #pg.time.delay(100)

                visitedSet.add(curr.pos)
                # Look at the neighbors
                random.shuffle(self.directions)
                for direction in self.directions:
                    x = curr.x+direction[0]
                    y = curr.y+direction[1]
                    position = Position(x, y, curr)
                    distance = abs(position.x-end[0]) + abs(position.y-end[1]) # Manhattan distance to goal(end)
                    if (not(position.pos in visitedSet) and self.inBounds(position.pos) and (not self.posToTile[position.pos].isWall)):
                        discovered.append((position, distance))
                        self.posToTile[position.pos].wasDiscovered = True
                        self.posToTile[position.pos].update()
                        self.posToTile[position.pos].draw()

    def Astar(self, start, end):
        visitedSet = set()
        discovered = [] # holds Position objects(row, col, prev) for tile

        first = Position(start[0], start[1])
        discovered.append((first, 0))
        while(len(discovered) > 0):
            # Get the position from  known positions with smallest manhattan distance to goal(end)
            minDistanceCost = math.inf
            for position, distanceCost in discovered:
                if (distanceCost < minDistanceCost):
                    curr = position
                    minDistanceCost = distanceCost
                    
            discovered.remove((curr, minDistanceCost))
            
            if (not (curr.pos in visitedSet)):
                # Get the actual tile using the map
                tile = self.posToTile[curr.pos]
                tile.visited = True

                if (curr.pos == start):
                    tile.isStart = True
                # Goal check
                if (curr.pos == end):
                    tile.isEnd = True
                    self.reconstructPath(curr)
                    return

                # So the search is animated as it is happening
                tile.update()
                tile.draw()
                #pg.time.delay(100)

                visitedSet.add(curr.pos)
                # Look at the neighbors
                random.shuffle(self.directions)
                for direction in self.directions:
                    x = curr.x+direction[0]
                    y = curr.y+direction[1]
                    position = Position(x, y, curr, cost=curr.cost+tile.Weight)
                    distanceCost = abs(position.x-end[0]) + abs(position.y-end[1]) + position.cost # Manhattan distance to goal(end)
                    if (not(position.pos in visitedSet) and self.inBounds(position.pos) and (not self.posToTile[position.pos].isWall)):
                        discovered.append((position, distanceCost))
                        self.posToTile[position.pos].wasDiscovered = True
                        self.posToTile[position.pos].update()
                        self.posToTile[position.pos].draw()


    def reset(self, clearWalls=True):
        for tile in self.allTiles:
            tile.visited = False
            tile.wasDiscovered = False
            tile.isStart = False
            tile.isEnd = False
            tile.inPath = False
            if (clearWalls):
                tile.isWall = False
                tile.Weight = 1
        self.update()
        self.draw()



class Position():

    def __init__(self, x, y, prev=None, depth=0, cost=0):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.prev = prev
        self.depth = depth
        self.cost = cost
    
    def __repr__(self):
        string = f'({self.x}, {self.y})   Prev:{self.prev}'
        return string


class Tile(pg.sprite.Sprite):

    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = RED
        self.tileSize = game.tile_size
        self.image = pg.Surface((self.tileSize, self.tileSize))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.visited = False
        self.isStart = False
        self.isEnd = False
        self.inPath = False
        self.wasDiscovered = False
        self.isWall = False
        self.Weight = 1
        self.game = game

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        self.game.drawGrid()
        pg.display.flip()

    def update(self):


        if self.visited:
            self.color = BLUE
        elif self.wasDiscovered:
            self.color = YELLOW
        elif self.Weight > 1:
            self.color = self.game.slider.color
        else:
            self.color = WHITE

        
        
        if self.isStart:
            self.color = GREEN
        elif self.isEnd:
            self.color = RED
        elif self.inPath:
            self.color = MAGENTA
        
        if self.isWall:
            self.color = BLACK

        self.image.fill(self.color)
        

class Button(pg.sprite.Sprite):

    def __init__(self, x, y, game, text):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.buttonWidth = 10*game.tile_size
        self.buttonHeight = 20
        self.image = pg.Surface((self.buttonWidth, self.buttonHeight))
        self.rect = self.image.get_rect()
        self.text = text
        fontStuff = pg.font.Font(pg.font.get_default_font(), 15)
        self.textSurface = fontStuff.render(text, False, BLACK)

            
    def draw(self):
        # Draw the colored box and the text
        pg.draw.rect(self.game.screen, RED, (self.x, self.y, self.buttonWidth, self.buttonHeight))
        self.game.screen.blit(self.textSurface, (self.x, self.y))


class Slider(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.lx = x
        self.ly = y
        self.bx = self.lx + 100
        self.by = self.ly
        self.game = game
        self.image = pg.Surface((100, 20))
        self.rect = self.image.get_rect()
        self.color = (self.by, 0, (self.bx-1250))
        

    def draw(self):
        pg.draw.rect(self.game.screen, BLACK, (self.lx, self.ly+self.game.tile_size//2, 200, 5))
        pg.draw.rect(self.game.screen, self.color, (self.bx, self.by, self.game.tile_size, self.game.tile_size))
    
    def update(self):
        self.color = (self.by, 0, (self.bx-1250))
        pos = pg.mouse.get_pos()
        x = pos[0]//self.game.tile_size
        
        
        #inbounds on right
        if x <= WIDTH//self.game.tile_size-self.game.tilesInButton:
            self.bx = WIDTH - 10*self.game.tile_size
        #inbounds on left
        elif pos[0] >= WIDTH-self.game.tile_size:
            self.bx = WIDTH-self.game.tile_size
        #if inbounds
        elif x > WIDTH//self.game.tile_size-self.game.tilesInButton and x < WIDTH:
            self.bx = pos[0]



g = Game()

while g.running:
    g.new()

pg.quit()