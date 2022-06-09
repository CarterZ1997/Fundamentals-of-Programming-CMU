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
        #ball radius is 9
        self.r = 9
        Colorball.colorList.append(self)

    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = self.color)

    def move(self, data):
        if self.speed.real >= data.friction:
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

    def checkScore(self, data):
        for hole in data.holes:
            if ((self.x - hole[0]) ** 2 + (self.y - hole[1]) ** 2) ** 0.5 <= data.holeRadius + 1:
                if self.color == "white":
                    data.isCueMove = False
                    data.cue = Colorball(data.leftSide + 150, data.height / 2, "white", data.leftSide + 150, data.height / 2, 0)
                if self.color == "black" and len(Colorball.colorList) != 2:
                    print("You can't pot black ball!")
                else:
                    #print("Score!")
                    Colorball.colorList.remove(self)
                    if len(Colorball.colorList) == 1:
                        print("You finished!")
                        if data.score < data.bestScore:
                            data.bestScore = data.score
                            writeFile(data.tf, str(data.bestScore))
                        Colorball.colorList = []
                        data.b1.destroy()
                        init(data)

    def checkWall(self, data):
        if (self.x <= data.leftSide + self.r) or (self.x >= data.rightSide - self.r):
            originalSourceX = self.sourceX
            self.sourceX = 2 * self.x - originalSourceX
        if (self.y >= data.bottomSide - self.r) or (self.y <= data.topSide + self.r):
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
    #initiate the mouse position
    data.motionPosn = (data.leftSide + 100, data.height / 2)
    data.leftPosn = (data.leftSide + 100, data.height / 2)
    data.isLeftPressed = False
    data.distance = 10
    data.track = (0, 0)
    data.force = 0
    # deal with ball movement
    data.speed = 1
    data.friction = 0.01 
    data.isCueMove = False
    data.mode = "splashScreen"
    #code cited from button-demo1.py, from the lecture superFun tkinter
    buttonFrame = Frame(data.root)
    data.b1 = Button(buttonFrame, text="help", command=lambda:onButton(data,1))
    data.b1.grid(row=0,column=1)
    buttonFrame.pack(side=BOTTOM)
    data.score = 0
    #data.bestScore = 100000
    data.P1 = PhotoImage(file="Picture1.gif")
    data.P2 = PhotoImage(file="Picture2.gif")
    data.tf = "best.txt"
    data.bestScore = int(openFile(data.tf))

######################
#Code cited http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-strings.html#basicFileIO
def openFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

##################
#code cited from button-demo1.py, from the lecture superFun tkinter

def onButton(data, buttonId):
    if (buttonId == 1): button1Pressed(data)


def button1Pressed(data):
    data.mode = "help"

####################################
# mode dispatcher
####################################

def mousePressed(mouseFn, event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   mouseFn(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGamekeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)

#################################
#Play Mode
#################################

#mouse motion code cited from the mouseEventsDemo.py, but modified
def mouseMotion(event, data):
    if data.mode == "playGame":
        data.motionPosn = (event.x, event.y)

def leftPressed(event, data):
    if data.mode == "playGame":
        data.isLeftPressed = True
        data.leftPosn = (event.x, event.y)
        data.track = data.leftPosn

def leftMoved(event, data):
    if data.mode == "playGame":
        if data.isLeftPressed:
            data.leftPosn = (event.x, event.y)
            data.distance = 10 + ((data.track[0] - data.leftPosn[0])**2 + (data.track[1] - data.leftPosn[1])**2) ** 0.5

def leftReleased(event, data):
    if data.mode == "playGame":
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
        data.score += 1

def playGamekeyPressed(event, data):
    pass

def overLap(data):
    for i in range(len(Colorball.colorList)):
        for j in range(i, len(Colorball.colorList)):
            ball1 = Colorball.colorList[i]
            ball2 = Colorball.colorList[j]
            if ball1 != ball2 and ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5 <= 18:
                ball1.sourceX = ball2.x
                ball1.sourceY = ball2.y
                ball2.sourceX = ball1.x
                ball2.sourceY = ball1.y
                if ball1.speed == 0 and ball2.speed != 0:
                    ball1.speed = ball2.speed / 1.5
                    ball2.speed = ball2.speed / 1.5
                if ball2.speed == 0 and ball1.speed != 0:
                    ball2.speed = ball1.speed / 1.5
                    ball1.speed = ball1.speed / 1.5
                if ball1.speed == 0 and ball2.speed == 0:
                    ball1.speed = 0.2
                    ball2.speed = 0.2
                else:
                    ball1.speed /= 1.3
                    ball2.speed /= 1.3
                ball1.move(data)
                ball2.move(data)

def playGameTimerFired(data):
    #check collision and collide
    for i in range(len(Colorball.colorList)):
        for j in range(i, len(Colorball.colorList)):
            ball1 = Colorball.colorList[i]
            ball2 = Colorball.colorList[j]
            if ball1 != ball2 and ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5 <= 18:
                ball1.collide(ball2)
                overLap(data)

    #move colorball
    for ball in Colorball.colorList:
        if ball.color != "white":
            ball.move(data)

    #check cue ball
    if data.isCueMove:
        if data.cue.speed == 0:
            data.isCueMove = False

    #check if scored:
    for ball in Colorball.colorList:
        ball.checkScore(data)

    #check if hit wall:
    for ball in Colorball.colorList:
        ball.checkWall(data)
        ball.move(data)

def playGameRedrawAll(canvas, data):
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
    drawArm(canvas, data)
    canvas.create_text(data.width / 4, 40, text = "Steps made: %d" % (data.score))
    canvas.create_text(data.width * 3 / 4, 40, text = "Best Game Step: %d" % (data.bestScore))

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
#Splash Screen Mode
###################################

def splashScreenMousePressed(event, data):
    pass

def splashScreenKeyPressed(event, data):
    if event.char == "p":
        data.mode = "playGame"

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
    canvas.create_text(data.width / 2, data.height / 4, text = "Play   Pool   Game!", fill = "blue", font = "Times 40 bold italic")
    #canvas.create_rectangle(data.width / 2 - 50, data.height / 2 - 20, data.width / 2 + 50, data.height / 2 + 20, fill = "white", width = 0)
    canvas.create_text(data.width / 2, data.height / 2, text = "Press P to Play", fill = "white", font = "Times 20 bold")
    canvas.create_image(data.width / 2, data.height / 4 * 3, image = data.P1)

####################################
# help mode
####################################

def helpMousePressed(event, data):
    pass

def helpKeyPressed(event, data):
    if event.char == "r":
        data.mode = "playGame"

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
    text = """
    Play Pool Instructions:
        Finish the game by pocketing all the color balls.
        Black ball has to be the last one to be pocketed.
        Try to finish the game in the least steps you can make.
        The numebr of steps you have made so far will be shown.
        The fewest number of steps you ever made will be shown as the best play."""
    canvas.create_text(10, 10, anchor = "nw", text = text, font = "Helvetica 20 bold italic", fill = "white")
    canvas.create_text(data.width / 2, data.height / 2, text = "Press R to play", font = "Times 20 bold", fill = "grey")
    canvas.create_image(data.width / 2, data.height / 4 * 3, image = data.P2)

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
        mousePressed(mouseFn, event, data)
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
    data.timerDelay = 10 # milliseconds
    root = Tk()
    data.root = root
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
