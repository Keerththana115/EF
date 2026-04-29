from tkinter import * # Module und Objekte aus Tkinter importieren
from tkinter import colorchooser #wird für die Farbauswahl verwendet, um ein Farbauswahlfenster zu erstellen.
from tkinter import filedialog # dient zum Öffnen und Speichern von Dialogfenstern.
from tkinter import messagebox # wird verwendet, um Informations- oder Fragefenster anzuzeigen.

# Ein grosser Teil des Codes stammt von folgendem Projekt: https://github.com/Vishesh-Pandey/paint-app-tkinter/blob/main/main.py


# Es wird ein Fenster mit dem Namen „Zeichenprogramm“ und der Grösse 1100 × 600 erstellt.
window = Tk()
window.title("Zeichenprogramm")
window.geometry("1100x600")


#--------------Variable---------------

# Liste der möglichen Pinsel und radiergrössen
options = [1,2,3,4,5,10,11,12,13,14,15]

# Werkzeugsgrösse wird am Anfang auf 1 gesetzt.
tool_size = IntVar()
tool_size.set(1)

# Werkzeugsfarbe wird am Anfang auf schwarz gesetzt.
tool_color = StringVar()
tool_color.set("black")

# Hintergrundsfarbe wird am Anfang auf weiss gesetzt.
bg_color = StringVar()
bg_color.set("white")

# Vorherige und aktuelle Punkt wird gespeichert (um eine Linie zu zeichnen).
prevPoint = [0,0]
currentPoint = [0,0] 

# speichert gelöschte und aktuelle Aktionen.
undo_stack= []
redo_stack =[]

#Aktuelle Strich
current_stroke = []


#---------------------Funktionen-------------------------

# welche Farbe verwendet wird und wie der Mauszeiger aussieht, wenn der Pinsel benutzt wird.
def useBrush():
    tool_color.set("black")
    canvas.config(cursor="cross")


# welche Farbe verwendet wird und wie der Mauszeiger aussieht, wenn der Radierer benutzt wird.
def useEraser():
    tool_color.set("white")
    canvas.config(cursor="dot")

# Öffnet Farbauswahl und setzt die gewählte Farbe als Zeichenfarbe
# Falls keine Farbe gewählt wird, bleibt Schwarz als Standard
def selectColor():
    selectedColor = colorchooser.askcolor("blue" , title="Farbe")
    if selectedColor[1] == None :
        tool_color.set("black")
    else:
        tool_color.set(selectedColor[1])


# Falls keine Farbe für den Hintergrund ausgewählt wird, bleibt der Hintergrund weiss.
# Ansonsten wird die ausgewählte Farbe als Hintergrundfarbe übernommen.
def changeBackground():
    selectedColor =  colorchooser.askcolor( title="Hintergrundfarbe")
    if selectedColor[1] == None :
        bg_color.set("white")
        #canvas["bg"]= bg_color.set("white")
        frame2["bg"]= bg_color.set("white")

    else:
        bg_color.set(selectedColor[1])
        canvas["bg"]= selectedColor[1]
        frame2["bg"]= selectedColor[1]
        
# Eine Aktion wird aus dem Undo-Stack entfernt und in den Redo-Stack verschoben,
# damit sie später wiederhergestellt werden kann.
# Dabei werden alle Segmente einer Linie gelöscht.
def undo():
    if undo_stack:
        stroke = undo_stack.pop()
        redo_stack.append(stroke)
        for item in stroke:
            canvas.delete(item[0])

# Falls etwas wiederhergestellt werden kann, wird der zuletzt rückgängig gemachte Strich
# neu auf dem Canvas gezeichnet.
# Da alte Canvas-IDs ungültig sind, müssen alle Segmente neu erstellt werden.
# Danach wird der Strich wieder in den Undo-Stack verschoben.
def redo():
    if redo_stack:
        stroke = redo_stack.pop()
        new_stroke = []
        for item in stroke:
            new_line = canvas.create_line(item[1], fill=item[2], width=item[3])
            new_stroke.append((new_line, item[1], item[2], item[3]))
        undo_stack.append(new_stroke)

# Zeichnet eine Linie zwischen dem vorherigen und dem aktuellen Mauspunkt.
# Solange die Maustaste gedrückt ist (B1-Motion), werden fortlaufend kleine Liniensegmente erstellt
# und zum aktuellen Strich (current_stroke) hinzugefügt.
# Wenn die Maustaste losgelassen wird, wird der gezeichnete Strich gespeichert,
# der Redo-Speicher gelöscht und der aktuelle Strich zurückgesetzt.
def paint(event):
    global prevPoint, currentPoint, current_stroke
    x = event.x
    y = event.y
    currentPoint = [x, y]
    if prevPoint != [0, 0] and prevPoint != currentPoint:
        coords = (prevPoint[0], prevPoint[1], currentPoint[0], currentPoint[1])
        color = tool_color.get()
        size = tool_size.get()
        line = canvas.create_line(coords, fill=color, width=size, capstyle= ROUND, joinstyle= ROUND)
        current_stroke.append((line, coords, color, size))

    prevPoint = currentPoint

    if event.type == "5":
        if current_stroke:
            undo_stack.append(current_stroke)
            redo_stack.clear()
            current_stroke = []

        prevPoint = [0, 0]

# Speichert den Canvas-Inhalt als PNG-Datei.
# Der Canvas wird zuerst als temporäre EPS-Datei zwischengespeichert,
# dann in PNG umgewandelt und die EPS-Datei danach gelöscht.
# Nach dem Speichern wird gefragt, ob das Bild direkt geöffnet werden soll.
def saveImage():
   try:
       fileLocation = filedialog.asksaveasfilename(defaultextension=".png")
       if fileLocation:
           canvas.postscript(file="temp.eps", colormode="color")
           from PIL import Image as PILImg
           import os
           img = PILImg.open("temp.eps")
           img.load()  # ← Bild komplett laden
           img.save(fileLocation, "PNG")
           img.close()  # ← Datei schliessen
           os.remove("temp.eps")
           showImage = messagebox.askyesno("Zeichenprogramm", "Wollen Sie das Bild öffnen?")
           if showImage:
               PILImg.open(fileLocation).show()
   except Exception as e:
       print(e)
       messagebox.showinfo("Zeichenprogramm", "Es ist ein Fehler aufgetreten!")

# Löscht den gesamten Inhalt der Zeichenfläche, falls der Benutzer bestätigt
def clear():
    if messagebox.askokcancel("Zeichenprogramm" , "Möchten Sie alles löschen?"):
        canvas.delete('all')

# Erstellt ein neues Projekt.
# Zuerst wird gefragt, ob das aktuelle Bild gespeichert werden soll.
def createNew():
    if messagebox.askyesno("Zeichenprogramm" , "Möchten Sie speichern bevor Sie alles löschen?"):
        saveImage()
    clear()

# Vergrössert die Zeichenfläche, indem alles etwas grösser dargestellt wird
zoom_factor = 1
def zoomIn():
    global zoom_factor
    zoom_factor *= 1.2
    canvas.scale("all", 0, 0, 1.2, 1.2)


# Verkleinert die Zeichenfläche, indem alles etwas kleiner dargestellt wird
def zoomOut():
    global zoom_factor
    zoom_factor *= 0.8
    canvas.scale("all", 0, 0, 0.8, 0.8)

# Verschiebt die gesamte Zeichenfläche mit den Pfeiltasten um 10 Pixel 
# Aus: https://www.youtube.com/watch?v=m17jsAfJBlc 
def moveUp(event):
    canvas.move("all", 0, -10)
def moveDown(event):  
    canvas.move("all", 0, 10)
def moveLeft(event):
    canvas.move("all", -10, 0)
def moveRight(event):
    canvas.move("all", 10, 0)



#--------------------Benutzeroberfläche----------------------------

# --- Werkzeugsbuttons ---
# Hauptframe für die gesamte obere Werkzeugleiste
frame1 = Frame(window, height=100, width=1100)
frame1.grid(row=0, column=0, sticky=NW)

# Frame für Pinsel und Radierer
toolsFrame = Frame(frame1, height=50, width=100, relief=SUNKEN, borderwidth=3)
toolsFrame.grid(row=0, column=0)

# Buttons für die Werkzeuge Pinsel und Radierer
brushButton = Button(toolsFrame, text="Pinsel 🖌️", bg="white", width=15, command=useBrush)
brushButton.grid(row=0, column=0)

eraserButton = Button(toolsFrame, text="Radierer 🧽", bg="white", width=15, command=useEraser)
eraserButton.grid(row=0, column=1)


# --- Pinsel- oder Radierer-grösse ---
# Dropdown-Menü zur Auswahl der Pinsel- oder Radiergrösse
sizeFrame = Frame(frame1, height=50, width=100, relief=SUNKEN, borderwidth=3, bg="white")
sizeFrame.grid(row=0, column=2)
sizeList = OptionMenu(sizeFrame, tool_size, *options)
sizeList.grid(row=0, column=0)
sizeLabel = Label(sizeFrame, text="Grösse", bg="white", width=10)
sizeLabel.grid(row=0, column=1)

# --- Farben ---
# Frame für Farb- und Hintergrundauswahl
colorBoxFrame = Frame(frame1, height=50, width=100, relief=SUNKEN, borderwidth=3)
colorBoxFrame.grid(row=0, column=4)

# Button zur Auswahl der Zeichenfarbe
colorBoxButton = Button(colorBoxFrame, text="Farbe", bg="white", width=15, command=selectColor)
colorBoxButton.grid(row=0, column=1)

# Button zur Auswahl der Hintergrundfarbe
bgColorButton = Button(colorBoxFrame, text="Hintergrundfarbe", bg="white", width=15, command=changeBackground)
bgColorButton.grid(row=0, column=7)

# --- Rückgängig und Wiederherstellen ---
# Frame für Rückgängig- und Wiederherstellen-Funktionen
undoRedoFrame = Frame(frame1, height=50, width=100, relief=SUNKEN, borderwidth=3)
undoRedoFrame.grid(row=0, column=5)
undoButton = Button(undoRedoFrame, text="Rückgängig", bg="white", width=15, command=undo)
undoButton.grid(row=0, column=0)
redoButton = Button(undoRedoFrame, text="Wiederherstellen", bg="white", width=15, command=redo)
redoButton.grid(row=0, column=1)


# ---hinein- und heraus-Zoomen ---
# Frame für Zoom-Funktionen
zoomInZoomOutFrame = Frame(frame1, height=50, width=100, relief=SUNKEN, borderwidth=3)
zoomInZoomOutFrame.grid(row=0, column=7)
zoomInButton = Button(zoomInZoomOutFrame, text="Hineinzoomen", width=15, bg="white", command=zoomIn)
zoomInButton.grid(row=0, column=0)
zoomOutButton = Button(zoomInZoomOutFrame, text="Herauszoomen", width=15, bg="white", command=zoomOut)
zoomOutButton.grid(row=0, column=1)


# ---Menüleiste ---
# Menüleiste für Datei-Funktionen. # Quelle: https://www.youtube.com/watch?v=cqL1FgPtMfg

menubar = Menu(window)
file = Menu(menubar, tearoff=0)
file.add_command(label="Neu", command=createNew)
file.add_command(label="Speichern", command=saveImage)
file.add_command(label="Löschen", command=clear)
file.add_separator()
file.add_command(label="Beenden", command=window.quit)
menubar.add_cascade(label="Datei", menu=file)
window.config(menu=menubar)


# --- Zeichenfläche ---
# Haupt-Zeichenbereich, in dem gezeichnet wird
frame2 = Frame(window, height=570, width=1100, bg="yellow")
frame2.grid(row=1, column=0)

# Canvas = Zeichenfläche
canvas = Canvas(frame2, height=570, width=1100, bg="white")
canvas.grid(row=0, column=0)

# Maussteuerung für Zeichnen
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)

# Pfeiltasten verschieben die Zeichenfläche
window.bind("<Up>", moveUp)
window.bind("<Down>", moveDown)
window.bind("<Left>", moveLeft)
window.bind("<Right>", moveRight)

# Fenstergrösse fixieren
window.resizable(False, False)

# Startet die Anwendung
window.mainloop()