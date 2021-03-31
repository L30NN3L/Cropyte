from PIL import Image as PILImage, ImageTk, ImageColor, ImageDraw
from tkinter import *
from tkinter import ttk, filedialog, colorchooser
import copy, os

gui = Tk()

image = None
y = None
x = None


colorSelector = None
colorBackground = None

listCoordenates = []

fileBasename = None

checkTest = IntVar()

def findEdgeB(coordX, j, originEdgeA):

    return (  image.getpixel((coordX,j)) == colorSelector and
                image.getpixel((coordX,j-1)) == colorSelector and
                image.getpixel((coordX,j-2)) == colorSelector and
                image.getpixel((coordX + 1,j - 1)) == colorBackground and
                image.getpixel((coordX+1,j)) == colorSelector and
                image.getpixel((coordX+2,j)) == colorSelector and
                image.getpixel((coordX+3,j)) == colorSelector and
                image.getpixel((coordX,j-3)) == colorSelector and
                originEdgeA != j)

def findEdgeA(coordX, j):

    return (  image.getpixel((coordX,j)) == colorSelector and
                    image.getpixel((coordX,j+1)) == colorSelector and
                    image.getpixel((coordX + 1,j)) == colorSelector and
                    image.getpixel((coordX+1,j+1)) == colorBackground and
                    image.getpixel((coordX + 2,j)) == colorSelector and
                    image.getpixel((coordX,j + 2)) == colorSelector and
                    image.getpixel((coordX,j + 3)) == colorSelector and 
                    image.getpixel((coordX + 3,j)) == colorSelector)


def findEdgeC(coordY, i):

    return (  image.getpixel((i,coordY)) == colorSelector and
                image.getpixel((i,coordY + 1)) == colorSelector and
                image.getpixel((i-1,coordY)) == colorSelector and
                image.getpixel((i-2,coordY)) == colorSelector and
                image.getpixel((i,coordY + 2)) == colorSelector and
                image.getpixel((i-1,coordY+1)) == colorBackground)


def itsRectangle(coords):

    if(coords['a'][0] == coords['b'][0] and
        coords['a'][1] == coords['c'][1] and
        coords['c'][0] == coords['d'][0] and
        coords['b'][1] == coords['d'][1]):
        return True

    return False


def findPixelsAandB(coordX, indexJ = 0):
    
    pixelsValues = {}

    originEdgeA = 0
    originEdgeB = 0

    foundEdgeA = False
    
    for j in range(indexJ, y):

        if (j < y - 2 and coordX < x - 2):

            if (  findEdgeA(coordX, j) and foundEdgeA == False ):

                    originEdgeA = j
                    pixelsValues['a'] = (coordX, originEdgeA)
                    foundEdgeA = True
            
            elif ( findEdgeA(coordX, j) and foundEdgeA == True):
                findPixelsAandB(coordX, j)

            if (findEdgeA and originEdgeA != 0):
                
                if ( findEdgeB(coordX, j, originEdgeA) ):
                        
                        originEdgeB = j
                        pixelsValues['b'] = (coordX, originEdgeB)
                        findPixelsCandD(originEdgeA, originEdgeB, pixelsValues, coordX + 1)

                        originEdgeA = 0
                        originEdgeB = 0
                        foundEdgeA = False
                        j = j + 1

    pass

def findPixelsCandD(originEdgeAy, originEdgeBy, pixelsValues ,indexI = 0):
    
    pixels = {}
    pixels['a'] = pixelsValues['a']
    pixels['b'] = pixelsValues['b']

    originEdgeC = 0

    for i in range(indexI, x):


        if (indexI < y - 2):
            
            if ( findEdgeC(originEdgeAy, i) ):
                
                originEdgeC = i
                pixels['c'] = (originEdgeC, originEdgeAy)

        if( originEdgeC != 0):
            
                pixels['d'] = (originEdgeC, originEdgeBy)

                originEdgeC = 0

                appendCoordinates(pixels)
                break

    pass


def appendCoordinates(values):

    coordinates = copy.deepcopy(values)
    
    listCoordenates.append(coordinates)

def reverseColor(color):

    r, g, b = color

    r = r-255
    g = g-255
    b = b-255

    return (abs(r), abs(g), abs(b))


def paintTest():
    global colorSelector, colorBackground, listCoordenates, image

    reverseSelector = reverseColor(colorSelector)
    reverseBackground = reverseColor(colorBackground)

    imageTest = image.copy()

    for coords in listCoordenates:
        paintFrames(imageTest, coords, reverseSelector, reverseBackground)

    imageTest.save('TestCrop.png')

def paintFrames(imageTest, coords, rs, rb):

    coordAx, coordAy = coords['a']
    coordBx, coordBy = coords['b']
    coordCx, coordCy = coords['c']
    coordDx, coordDy = coords['d']

    imageTest.putpixel(coords['a'], rs)
    imageTest.putpixel((coordAx, coordAy + 1), rs)
    imageTest.putpixel((coordAx + 1, coordAy), rs)
    imageTest.putpixel((coordAx + 1, coordAy + 1), rb)

    imageTest.putpixel(coords['b'], rs)
    imageTest.putpixel((coordBx, coordBy - 1), rs)
    imageTest.putpixel((coordBx + 1, coordBy), rs)
    imageTest.putpixel((coordBx + 1, coordBy - 1), rb)

    imageTest.putpixel(coords['c'], rs)
    imageTest.putpixel((coordCx - 1, coordCy), rs)
    imageTest.putpixel((coordCx, coordCy + 1), rs)
    imageTest.putpixel((coordCx - 1, coordCy + 1), rb)

    imageTest.putpixel(coords['d'], rs)
    imageTest.putpixel((coordDx - 1, coordDy), rs)
    imageTest.putpixel((coordDx, coordDy - 1), rs)
    imageTest.putpixel((coordDx - 1, coordDy - 1), rb)


def isOdd(number):

    if (number % 2 != 0):
        return True
    
    return False

def organizeFrames(listCoordenates):

    return sorted(listCoordenates, key = lambda o: o['a'][1])

def paintCropped(image,width,height):

    newImage = PILImage.new("RGBA",image.size)

    pixelMap = image.load()

    pixelsNew = newImage.load()

    for w in range(width):
        for h in range(height):
            pixelsNew[w,h] = pixelMap[w,h]
            if(pixelMap[w,h] == (113,38,38)):
                pixelsNew[w,h] = (0,0,0,0)

    return newImage

def calculateColumnsLines(quantityFrames):
    
    qtdF = quantityFrames

    divisors = []

    columns = lines = 0

    for n in range(2,qtdF):
        
        if(qtdF % n == 0):
            divisors.append(n)

    if(len(divisors) >= 2):
        
        divisors.reverse()
        columns = divisors.pop()
        divisors.reverse()

        for divisor in divisors:
            if divisors:
                lines = divisors.pop()
                if(lines * columns == qtdF):
                    break
            else:
                break

    elif(len(divisors) == 1):
        
        lines = columns = divisors.pop()
    
    elif not divisors:

        return calculateColumnsLines(qtdF+1)

    return (columns, lines)
    
def writeFileDetails(biggerX, biggerY, columns, lines, Nwidth, Nheight):

    f = open("detailsNewFile.txt", "w")
    f.write("New Frame Size \n")
    f.write("X: " +str(biggerX)+ " \n")
    f.write("Y: " +str(biggerY)+ " \n")
    
    f.write("\nColumns: " +str(columns)+ "\nLines: " +str(lines)+ "\n")

    f.write("Width New File: " +str(Nwidth)+ "\n")
    f.write("Height New File: " +str(Nheight)+ "\n")

    pass

def calculateFrames():
    global fileBasename

    biggerX = 0
    biggerY = 0

    deltaX = 0
    deltaY = 0

    for square in listCoordenates:

        deltaX = square['c'][0] - square['a'][0]

        if deltaX > biggerX:
            biggerX = deltaX

        deltaY =  square['b'][1] - square['a'][1]

        if deltaY > biggerY:
            biggerY = deltaY

    biggerX = round(biggerX + 0.5)
    biggerY = round(biggerY + 0.5)

    columns, lines = calculateColumnsLines(len(listCoordenates)) 

    newImageX = biggerX * columns
    newImageY = biggerY * lines

    writeFileDetails(biggerX,biggerY,columns,lines,newImageX,newImageY)

    newImage = PILImage.new("RGBA", (newImageX, newImageY), (0,0,0,0))

    for line in range(lines):
        
        for column in range(columns):

            if(listCoordenates):

                coordinates = listCoordenates.pop()

                top = coordinates['a'][0] + 1
                left = coordinates['a'][1] + 1
                right = coordinates['d'][0]
                bottom = coordinates['d'][1]

                img_crop = image.crop((top,left,right,bottom))

                img_x, img_y = img_crop.size

                img_crop = paintCropped(img_crop,img_x,img_y)

                offset = (((biggerX - img_x) // 2) + biggerX * column,
                ((biggerY - img_y) // 2) + biggerY * line)

                newImage.paste(img_crop,offset)
            else:
                break
    
    fileNameEdit = fileBasename.split('.')[0]
    fileNameEdit += '-CropytEdition.png'

    newImage.save(fileNameEdit)
    pass

def startAlgorithm():
    global listCoordenates

    if(image != None and 
       x != None and
       y != None and
       colorSelector != None and
       colorBackground != None):

        for coordX in range(x):
            findPixelsAandB(coordX)

        listCoordenates = organizeFrames(listCoordenates)

        listCoordenates.reverse()

        if(checkTest.get()):
            paintTest()
            
        calculateFrames()

    pass



imageSprite = None
gui.panelSprite = None
panelSprite_w = 300
panelSprite_h = 300
# gui.image = None
# gui.selectorColor = None
# gui.backgroundColor = None

gui.title("Cropyte")
gui.iconbitmap('images/rocket.ico')

frameBase = ttk.Frame(gui)

frameImage = ttk.LabelFrame(frameBase, text= "SpriteSheet")

canvas = Canvas(frameImage, width = panelSprite_w, height = panelSprite_h)

frameBtnDialog = ttk.LabelFrame(frameBase, text= "Import SpritSheet")
frameColors = ttk.LabelFrame(frameBase, text= "Especify the colors")
frameStart = ttk.Frame(frameBase)
frameBaseBoard = ttk.Frame(frameBase)
labelemail = ttk.Label(frameBaseBoard,text = "leonnelcode@gmail.com")
checkBoxTest = ttk.Checkbutton(frameBaseBoard, text="TestCrop", variable=checkTest)

def resizeImage(imageSprite):
    img_x, img_y = imageSprite.size
    for n in range(1,10):
        resize_x = img_x // n 
        resize_y = img_y // n 
        if((resize_x <= panelSprite_w) and (resize_y <= panelSprite_h)):
            imageSprite = imageSprite.resize((resize_x,resize_y), PILImage.ANTIALIAS)
            break
    return imageSprite 

def openFile():
    global image, x, y, fileBasename
    
    filename = filedialog.askopenfilename(initialdir = "/", title="Select A SpriteSheet",
        filetypes = (("png files","*.png"),("all files","*.*")) )

    image = PILImage.open(filename)
    
    x, y = image.size

    fileBasename = os.path.basename(filename)
    
    imageSprite = resizeImage(image)
    resize_w, resize_h = imageSprite.size
    gui.panelSprite = ImageTk.PhotoImage(imageSprite)
    canvas.create_image(panelSprite_w / 2 - resize_w / 2,
                         panelSprite_h / 2 - resize_h / 2, 
                         anchor=NW, image=gui.panelSprite)

btnDialogFile = ttk.Button(frameBtnDialog, text = "Import", command=openFile)

selectorCLabel = ttk.Label(frameColors, text= "Selector Color")
backgroundCLabel = ttk.Label(frameColors, text= "Background Color")

def chooseChangeColor(button,id):
    global colorSelector, colorBackground
    color = colorchooser.askcolor()
    button.configure(bg=color[1])
    if(id == 1):
        colorSelector = color[0]
    else:
        colorBackground = color[0]
    pass

btnSelectorColor = Button(frameColors, bd = 2, relief=RIDGE, width=3, 
                            bg="#FF0000", command = lambda: chooseChangeColor(btnSelectorColor,1))

btnBackgroundColor = Button(frameColors, bd = 2, relief=RIDGE, width=3, 
                            bg="#00FF00", command = lambda: chooseChangeColor(btnBackgroundColor,2))

btnStart = Button(frameStart, text="Start", command=startAlgorithm)

frameBase.grid(column=0, row=0)
frameImage.grid(column=0,row=0)
canvas.pack()
frameBtnDialog.grid(column=0, row=1)
frameColors.grid(column=0, row=2)
frameStart.grid(column=0, row=3)
frameBaseBoard.grid(column=0, row=4)
btnDialogFile.pack()
selectorCLabel.grid(column=0, row=0)
backgroundCLabel.grid(column=0, row=1)
btnSelectorColor.grid(column=1, row=0)
btnBackgroundColor.grid(column=1, row=1)
btnStart.pack()
labelemail.pack(side=LEFT)
checkBoxTest.pack(side=RIGHT)


gui.mainloop()