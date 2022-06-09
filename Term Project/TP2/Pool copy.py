import random, math
from tkinter import *

####################################
#15112 Term Project
#Shaojie Zhang
#Section B
####################################
#Pool Game!
####################################

class Colorball(object):
    colorList = []
    def __init__(self, x, y, color, sourceX, sourceY, speed):
        self.x = x
        self.y = y
        self.color = color
        self.sourceX = sourceX
        self.sourceY = sourceY
        self.speed = speed
        #ball radius is 10
        self.r = 10
        Colorball.colorList.append(self)

    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = self.color)

    def move(self, data):
        if self.speed >= data.friction:
            self.speed -= data.friction
            speed = self.speed / 10 * data.force
            vector = (self.x - self.sourceX, self.y - self.sourceY)
            norm = (vector[0]**2 + vector[1]**2) ** 0.5
            self.x += speed / norm * vector[0]
            self.y += speed / norm * vector[1]
        else:
            self.speed = 0


    def collide(self, other):#take in self, other and output the new data
        vectorA = (other.x - self.x, other.y - self.y)
        vectorB = (self.x - self.sourceX, self.y - self.sourceY)
        vectorC = (vectorB[0] - vectorA[0], vectorA[0] - vectorA[1])
        normA = (vectorA[0] ** 2 + vectorA[1] ** 2) ** 0.5
        normB = (vectorB[0] ** 2 + vectorB[1] ** 2) ** 0.5
        if normA * normB != 0:
            cosAngle = (vectorA[0] * vectorB[0] + vectorA[1] * vectorB[1]) / (normA * normB)
            sinAngle = (1 - cosAngle ** 2) ** 0.5
            other.speed = self.speed * cosAngle
            other.sourceX = self.x
            other.sourceY = self.y
            self.speed = self.speed * sinAngle
            self.sourceX = self.x - vectorC[0]
            self.sourceY = self.y - vectorC[1]
        if normA * normB == 0:
            other.speed = self.speed / 2
            other.sourceX = self.x
            other.sourceY = self.y
            self.speed = self.speed / 2
            self.sourceX = other.x
            self.sourceY = other.y

        #!!! take care of the heads on

    def checkScore(self, data):
        for hole in data.holes:
            if ((self.x - hole[0]) ** 2 + (self.y - hole[1]) ** 2) ** 0.5 <= self.r:
                if self.color == "white":
                    print("GameOver!")
                else:
                    print("Score!")

    def checkWall(self, data):
        if (self.x <= data.leftSide + self.r) or (self.x >= data.rightSide - self.r):
            print("checked x")
            originalSourceX = self.sourceX
            self.sourceX = 2 * self.x - originalSourceX
        if (self.y >= data.bottomSide - self.r) or (self.y <= data.topSide + self.r):
            print("checked y")
            originalSourceY = self.sourceY
            self.sourceY = 2 * self.y - originalSourceY



    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.color == other.color) and (self.sourceX == other.sourceX) and (self.sourceY == other.sourceY) and (self.speed == other.speed)


def init(data):
    #define all the data for the pool table
    data.width = 800
    data.height = 500
    data.sideMargin = 100
    data.topMargin = 75
    #define the edge size
    data.edge = 15
    data.leftSide = data.sideMargin + data.edge
    data.topSide = data.topMargin + data.edge
    data.rightSide = data.width - data.sideMargin - data.edge
    data.bottomSide = data.height - data.topMargin - data.edge
    ###! If time, draw the shaded region next to the edges
    #draw the holes by first storing their centers(tuple) in a list
    data.holeRadius = 12
    data.topMidHole = (data.width / 2, data.topSide + 5)
    data.bottomMidHole = (data.width / 2, data.bottomSide - 5)
    data.topLeft = (data.leftSide + 5, data.topSide + 5)
    data.bottomLeft = (data.leftSide + 5, data.bottomSide - 5)
    data.topRight = (data.rightSide - 5, data.topSide + 5)
    data.bottomRight = (data.rightSide - 5, data.bottomSide - 5)
    data.holes = [data.topMidHole, data.bottomMidHole, data.topLeft, 
                data.bottomLeft, data.topRight, data.bottomRight]
    #define a cue ball
    data.ballRadius = 10
    data.cue = Colorball(data.leftSide + 150, data.height / 2, "white", data.leftSide + 150, data.height / 2, 0)
    # data.cueX = data.leftSide + 150
    # data.cueY = data.height / 2
    data.blackBall = Colorball(data.rightSide - 150, data.height / 2, "black", 0, 0, 0)
    data.c1 = Colorball(data.rightSide - 150, data.height / 2 - 2 * data.ballRadius, "yellow", 0, 0, 0)
    data.c2 = Colorball(data.rightSide - 150, data.height / 2 + 2 * data.ballRadius, "red", 0, 0, 0)
    data.c3 = Colorball(data.rightSide - 150 - math.sqrt(3) * data.ballRadius, data.height / 2 - data.ballRadius, "red", 0, 0, 0)
    data.c4 = Colorball(data.rightSide - 150 - math.sqrt(3) * data.ballRadius, data.height / 2 + data.ballRadius, "yellow", 0, 0, 0)
    data.c5 = Colorball(data.rightSide - 150 - 2 * math.sqrt(3) * data.ballRadius, data.height / 2, "yellow", 0, 0, 0)
    data.c6 = Colorball(data.rightSide - 150 + math.sqrt(3) * data.ballRadius, data.height / 2 - 3 * data.ballRadius, "red", 0, 0, 0)
    data.c7 = Colorball(data.rightSide - 150 + math.sqrt(3) * data.ballRadius, data.height / 2 - data.ballRadius, "yellow", 0, 0, 0)
    data.c8 = Colorball(data.rightSide - 150 + math.sqrt(3) * data.ballRadius, data.height / 2 + data.ballRadius, "red", 0, 0, 0)
    data.c9 = Colorball(data.rightSide - 150 + math.sqrt(3) * data.ballRadius, data.height / 2 + 3 * data.ballRadius, "yellow", 0, 0, 0)
    data.c10 = Colorball(data.rightSide - 150 + 2 * math.sqrt(3) * data.ballRadius, data.height / 2 - 4 * data.ballRadius, "red", 0, 0, 0)
    data.c11 = Colorball(data.rightSide - 150 + 2 * math.sqrt(3) * data.ballRadius, data.height / 2 - 2 * data.ballRadius, "yellow", 0, 0, 0)
    data.c12 = Colorball(data.rightSide - 150 + 2 * math.sqrt(3) * data.ballRadius, data.height / 2, "red", 0, 0, 0)
    data.c13 = Colorball(data.rightSide - 150 + 2 * math.sqrt(3) * data.ballRadius, data.height / 2 + 2 * data.ballRadius, "yellow", 0, 0, 0)
    data.c14 = Colorball(data.rightSide - 150 + 2 * math.sqrt(3) * data.ballRadius, data.height / 2 + 4 * data.ballRadius, "red", 0, 0, 0)
    # initiate the mouse position
    data.motionPosn = (data.leftSide + 100, data.height / 2)
    data.leftPosn = (data.leftSide + 100, data.height / 2)#i think this value does not really matter
    data.isLeftPressed = False
    data.distance = 10
    data.track = (0, 0)
    data.force = 0
    # deal with ball movement
    data.speed = 10#change this!!
    data.friction = 1 #change this?
    data.isCueMove = False

#mouse motion code cited from the mouseEventsDemo.py, but modified
def mouseMotion(event, data):
    data.motionPosn = (event.x, event.y)

def leftPressed(event, data):
    data.isLeftPressed = True
    data.leftPosn = (event.x, event.y)
    data.track = data.leftPosn

def leftMoved(event, data):
    if data.isLeftPressed:
        data.leftPosn = (event.x, event.y)
        data.distance = 10 + ((data.track[0] - data.leftPosn[0])**2 + (data.track[1] - data.leftPosn[1])**2) ** 0.5

def leftReleased(event, data):
    if data.isLeftPressed:
        data.leftPosn = (event.x, event.y)
    data.isLeftPressed = False
    data.force = data.distance
    data.distance = 10
    data.cue.speed = data.speed
    data.cue.sourceX = data.leftPosn[0]
    data.cue.sourceY = data.leftPosn[1]
    data.cue.move( data)
    data.isCueMove = True
    #data.cue.speed = 10
######

def keyPressed(event, data):
    pass

def timerFired(data):
    #####Wrong
    for i in range(len(Colorball.colorList)):
        for j in range(i, len(Colorball.colorList)):
            
            ball1 = Colorball.colorList[i]
            ball2 = Colorball.colorList[j]
            if ball1 != ball2 and ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5 <= 20:
                #print("Collising", ball1.color, ball2.color)
                #print("ball1SourceX, ball1SourceY", ball1.sourceX, ball1.sourceY)
                ball1.collide(ball2)
                #print("ball1SourceX, ball1SourceY", ball1.sourceX, ball1.sourceY)

    # for ball in Colorball.colorList:
    #     ball.checkWall(data)
    
    for ball in Colorball.colorList:
        if ball.color != "white":
            ball.move(data)

    if data.isCueMove:
        # data.cue.checkWall(data)
        # data.cue.sourceX = data.leftPosn[0]
        # data.cue.sourceY = data.leftPosn[1]
        # data.cue.move(data)
        # if data.cue.speed >= data.friction:
        #     data.cue.speed -= data.friction
        if data.cue.speed == 0:
            data.isCueMove = False

    ##check if scored:
    for ball in Colorball.colorList:
        ball.checkScore(data)

    ##check if hit wall:
    for ball in Colorball.colorList:
        ball.checkWall(data)
        ball.move(data)

def redrawAll(canvas, data):
    #draw the pool table
    canvas.create_rectangle(data.sideMargin, 
                        data.topMargin, data.width - data.sideMargin, 
                        data.height - data.topMargin, fill = "saddlebrown")
    #draw out the pool table edge, get the inside part
    x1, y1 = data.leftSide, data.topSide
    x2, y2 = data.rightSide, data.bottomSide
    canvas.create_rectangle(x1, y1, x2, y2, width = 1, fill = "darkgreen")
    #draw the holes
    drawHoles(canvas, data)
    #draw cue ball
    canvas. create_oval(data.cue.x - data.ballRadius, data.cue.y - data.ballRadius,
                     data.cue.x + data.ballRadius, data.cue.y + data.ballRadius, 
                     fill = "white")
    #draw colorballs
    for colorball in Colorball.colorList:
        colorball.draw(canvas)
    #draw the arm with data.motionPosn
    ###! draw the arm if all movement finishes
    drawArm(canvas, data)

def drawHoles(canvas, data):
    for hole in data.holes:
        cx, cy = hole[0], hole[1]
        r = data.holeRadius
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = "black")

def drawArm(canvas, data):
    if not data.isCueMove:
        if not data.isLeftPressed:
            mouseX = data.motionPosn[0]
            mouseY = data.motionPosn[1]
        if data.isLeftPressed:
            mouseX = data.leftPosn[0]
            mouseY = data.leftPosn[1]
        if mouseX < data.cue.x:
            angle = math.atan((data.cue.y - mouseY) / (data.cue.x - mouseX))
            sin = math.sin(angle)
            cos = math.cos(angle)
            tempY = data.cue.y - (10 + data.distance) * sin
            tempX = data.cue.x - (10 + data.distance) * cos
            p1x = tempX - 4 * sin
            p1y = tempY + 4 * cos
            p2x = tempX + 4 * sin
            p2y = tempY - 4 * cos
            temp1Y = data.cue.y - (110 + data.distance) * sin
            temp1X = data.cue.x - (110 + data.distance) * cos
            p4x = temp1X - 4 * sin
            p4y = temp1Y + 4 * cos
            p3x = temp1X + 4 * sin
            p3y = temp1Y - 4 * cos
            canvas.create_polygon(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y, fill = "orange")
        if mouseX > data.cue.x:
            angle = math.atan((data.cue.y - mouseY) / (mouseX - data.cue.x))
            sin = math.sin(angle)
            cos = math.cos(angle)
            tempY = data.cue.y - (10 + data.distance) * sin
            tempX = data.cue.x + (10 + data.distance) * cos
            p1x = tempX - 4 * sin
            p1y = tempY - 4 * cos
            p2x = tempX + 4 * sin
            p2y = tempY + 4 * cos
            temp1Y = data.cue.y - (110 + data.distance) * sin
            temp1X = data.cue.x + (110 + data.distance) * cos
            p4x = temp1X - 4 * sin
            p4y = temp1Y - 4 * cos
            p3x = temp1X + 4 * sin
            p3y = temp1Y + 4 * cos
            canvas.create_polygon(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y, fill = "orange")
        if mouseX == data.cue.x:
            if mouseY <= data.cue.y:
                canvas.create_rectangle(data.cue.x - 4, data.cue.y - (110 + data.distance), data.cue.x + 4, data.cue.y - (10 + data.distance), fill = "orange", width = 0)
            else:
                canvas.create_rectangle(data.cue.x - 4, data.cue.y + (10 + data.distance), data.cue.x + 4, data.cue.y + (110 + data.distance), fill = "orange", width = 0)


####################################
# use the run function as-is
####################################
# taken from the lecture notes: https://cs112.github.io/notes/notes4-2.html
def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    # the button taken from the mouseEventsDemo.py
    root.bind("<Button-1>", lambda event:
                            mouseWrapper(leftPressed, event, canvas, data))
    canvas.bind("<Motion>", lambda event:
                            mouseWrapper(mouseMotion, event, canvas, data))
    canvas.bind("<B1-Motion>", lambda event:
                            mouseWrapper(leftMoved, event, canvas, data))
    root.bind("<B1-ButtonRelease>", lambda event:
                            mouseWrapper(leftReleased, event, canvas, data))
    # root.bind("<Button-1>", lambda event:
    #                         mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 500)
