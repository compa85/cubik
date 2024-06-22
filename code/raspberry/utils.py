# ============================ LIBRARIES =============================
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import os.path
import json
from rubikscolorresolver.solver import RubiksColorSolverGeneric
import twophase.solver as solver
# commentare le seguenti due righe se non si sta utilizzando un raspberry
from picamera2 import Picamera2
from libcamera import controls


# ========================== CHECK VERTICES ==========================
# funzione per controllare se i vertici sono di un cubo 
def checkVertices(vertices):
  # controllo se i vertici sono 7
  if len(vertices) == 7:
    # calcolo l'inviluppo convesso dei vertici
    convexHull = cv.convexHull(np.array(vertices), True)
    # controllo se i punti presenti nell'inviluppo sono 6
    if(len(convexHull) == 6):
      return True
    else:
      return False
  else:
    return False


# ============================ SAVE FACES ============================
# funzione per salvare le facce del cubo in un json
def saveFaces(faces, path):
  with open(path, "w") as file:
    jsonData = json.dumps(faces, default=int)
    file.write(jsonData)


# ============================ LOAD FACES ============================
# funzione per caricare le facce del cubo salvate in un json
def loadFaces(path):
  if os.path.exists(path):
    with open(path, "r") as file:
      jsonData = file.read()
      faces = json.loads(jsonData)
      tmpFaces = []
      for i, face in enumerate(faces):
        tmpFaces.append([tuple(face) for face in faces[i]])
    return tmpFaces[0], tmpFaces[1], tmpFaces[2]
  else:
    return


# ============================ VIEW POINTS ===========================
# funzione per visualizzare un insieme di punti su un piano cartesiano, numerati in base al loro indice dell'array
def viewPoints(points):
  x = [p[0] for p in points]
  y = [p[1] for p in points]
  plt.plot(x, y, marker='o', linestyle='', color='green')
  for i in range(len(points)):
    plt.text(x[i], y[i], i, fontsize=10, ha='left', va='top')
  # plt.xlim(0, 1920)
  # plt.ylim(0, 1080)
  plt.gca().invert_yaxis()
  plt.grid(True)
  plt.show()


# ============================ VIEW FACES ============================
# funzione per visualizzare in un frame le 3 facce adiacenti del cubo
def viewFaces(frame, faces):
  face1, face2, face3 = faces

  # disegno le linee, aggiungendo il primo vertice alla fine di ogni faccia, così da chiuderla
  cv.polylines(frame, np.array([face1 + [face1[0]]]), False, (255, 0, 0), 4)
  cv.polylines(frame, np.array([face2 + [face2[0]]]), False, (0, 255, 0), 4)
  cv.polylines(frame, np.array([face3 + [face3[0]]]), False, (0, 0, 255), 4)

  # cv.fillPoly(frame, np.array([face1 + [face1[0]]]), (255, 0, 0))
  # cv.fillPoly(frame, np.array([face2 + [face2[0]]]), (0, 255, 0))
  # cv.fillPoly(frame, np.array([face3 + [face3[0]]]), (0, 0, 255))


# ========================= VIEW FACE COLORS =========================
# funzione per visualizzare in un frame i colori delle facelet di una faccia
def viewFaceColors(frame, facelet, faceletColors):
  for i in range(len(faceletColors)):
    cv.fillPoly(frame, np.array([facelet[i]]), faceletColors[i])


# ========================== COLORS TO JSON ==========================
# funzione per convertire l'array di colori rgb delle facelet di ogni faccia in un json
def facesColorsToJson(upperColors, leftColors, frontColors, rightColors, backColors, downColors):
  colors = upperColors + leftColors + frontColors + rightColors + backColors + downColors
  json_dict = {str(index+1): list(value) for index, value in enumerate(colors)}
  return json.dumps(json_dict)


# ========================== CONVERT COLORS ==========================
# funzione per convertire un colore da rgb a bgr o viceversa
def convertRgbBgr(rgb):
  # controllo se la tupla rgb abbia effetivamente soltanto 3 o 4 elementi (4 se viene inclusa la trasparenza)
  if len(rgb) == 3 or len(rgb) == 4:
    return (rgb[2], rgb[1], rgb[0])
  else:
    return


# ============================= DISTANCE =============================
# funzione per il calcolo della distanza tra due punti (a e b)
def distance(a, b):
  return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# ============================= INTERSECT ============================
# funzione per il calcolo del punto di intersezione di due segmenti (seg1 e seg2)
def intersect(seg1, seg2):
  # inizializzo gli estremi di ciascun segmento
  a = seg1[0]
  b = seg1[1]
  c = seg2[0]
  d = seg2[1]

  # retta AB rappresentata come a1x + b1y = c1
  a1 = b[1] - a[1]
  b1 = a[0] - b[0]
  c1 = a1*(a[0]) + b1*(a[1])

  # retta CD rappresentata come a2x + b2y = c2
  a2 = d[1] - c[1]
  b2 = c[0] - d[0]
  c2 = a2*(c[0]) + b2*(c[1])

  determinant = a1 * b2 - a2 * b1

  # se il determinante è 0, le rette sono parallele
  if (determinant == 0):
    return None
  else:
    # calcolo le coordinate del punto utilizzando il metodo di Cramer
    x = (b2*c1 - b1*c2) / determinant
    y = (a1*c2 - a2*c1) / determinant
    return (x, y)
  

# ============================ SORT POINTS ===========================
# funzione per ordinare in senso orario o antiorario un insieme di punti nel piano
def sortPoints(points, clockwise = True):
  points = np.array(points)
  # calcolo il centro medio dei punti
  cx, cy = points.mean(0)
  x, y = points.T
  # calcolo gli angoli rispetto al centro medio dei punti
  angles = np.arctan2(x-cx, y-cy)
  # se l'ordinamento è in senso orario, inverto gli angoli
  if(clockwise):
    angles = -angles
  # ottengo gli indici degli angoli ordinati
  indices = np.argsort(angles)
  # trovo l'indice del punto con la y minore
  minY = np.argmin(y)
  # trovo l'indice del punto con l'angolo minore
  firstIndex = np.where(indices == minY)[0][0]
  # ruoto gli indici in modo che il punto con y minore sia il primo
  indices = np.roll(indices, -firstIndex)
  # ordino i punti in base agli indici
  points = points[indices]
  # converto points in un array di tuple
  points = [tuple(point) for point in points]
  return points


# ============================ GET CAMERA ============================
# funzione per ottenere una camera in base alla tipologia: quella di sistema (system) o una raspberry camera (raspi)
def getCamera(type, number):
  if type == "system":
    camera = cv.VideoCapture(number)
  elif type == "raspi":
    camera = Picamera2(number)
    cameraConfig = camera.create_preview_configuration({"format": "RGB888", "size": (1920, 1080)})
    camera.configure(cameraConfig)
    camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    # camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 9.0})
    camera.start()
  return camera


# ============================ GET FRAME =============================
# funzione per ottenere una frame
def getFrame(camera):
  # controllo se camera è un istanza di VideoCapture o di Picamera2, al fine di catturare il frame nel modo corretto
  if isinstance(camera, cv.VideoCapture) and camera.isOpened():
    ret, frame = camera.read()
  elif isinstance(camera, Picamera2):
    frame = camera.capture_array()
  return frame


# ============================ MASK ARMS =============================
# funzione per rimuovere le braccia che agganciano il cubo dal frame (presupponendo siano nere)
def maskArms(frame):
  # definisco il range di colori da rimuovere 
  lowerBlack = np.array([0, 0, 0]) 
  upperBlack = np.array([60, 80, 80])
  # creo una maschera
  mask = cv.inRange(frame, lowerBlack, upperBlack)
  # aggiungo il canale alfa al frame
  result = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
  # imposto l'area della maschera trasparente
  result[mask != 0, 3] = 0
  return result


# =========================== AVERAGE COLOR ==========================
# funzione per calcolare la media di una roi
def averageColor(roi):
  # estraggo i canali bgr e il canale alfa
  b, g, r, a = cv.split(roi)
  # creo una maschera per i pixel non trasparenti
  mask = a > 0
  # calcolo la media dei pixel non trasparenti per ciascun canale
  media_b = np.mean(b[mask])
  media_g = np.mean(g[mask])
  media_r = np.mean(r[mask])
  # combino le medie in un'unica variabile
  mean = (media_b, media_g, media_r)
  return mean


# ========================== MOUSE CALLBACK ==========================
# funzione per aggiungere il vertice cliccato all'array vertices
def mouseCallback(event, x, y, flags, state):  
  # se viene premuto il tasto sinistro del mouse
  if event == cv.EVENT_LBUTTONDOWN:
    # controllo se si è cliccato su un vertice già presente
    for index, vertex in enumerate(state["vertices"]):
      distance = ((x - vertex[0]) ** 2 + (y - vertex[1]) ** 2) ** 0.5
      if distance <= 30:
        state["draggingVertex"] = index
        break
      
    if state["draggingVertex"] == None and len(state["vertices"]) < 7:
      state["vertices"].append((x, y))
  
  # se si sta muovendo il mouse mentre è premuto il tasto sinistro
  elif event == cv.EVENT_MOUSEMOVE:
    if state["draggingVertex"] != None:
      state["vertices"][state["draggingVertex"]] = (x, y)
      state["faces"] = None
            
  # se viene rilasciato il tasto sinistro del mouse
  elif event == cv.EVENT_LBUTTONUP:
    state["draggingVertex"] = None


# ========================== SELECT VERTICES =========================
# funzione per selezionare i vertici del cubo. Se la posizione della camera è 0, il frame viene ruotato
def selectVertices(camera, cameraPosition):
  # dizionario utilizzato per passare i valori necessari a mouseCallback()
  state = {
    "vertices": [],
    "draggingVertex": None,
    "faces": None
  }
  
  cv.namedWindow("Configuration")
  cv.setMouseCallback("Configuration", mouseCallback, state)

  while True:
    frame = getFrame(camera)
    
    # disegno i vertici
    for vertex in state["vertices"]:
      cv.circle(frame, vertex, 10, (0, 255, 0), 2)
    
    if(len(state["vertices"]) == 7):
      if state["faces"] == None:
        state["faces"] = findFaces(state["vertices"], cameraPosition)
      viewFaces(frame, state["faces"])

    cv.imshow("Configuration", frame)

    # aspetto un input dalla tastiera per 5 millisecondi
    key = cv.waitKey(5)
    # se è stata premuta la c, i vertici selezionati vengono cancellati
    if key == ord("c"):
      state["vertices"] = []
      state["faces"] = None
    # se è stato premuto l'invio, vengono ritornati i vertici selezionati (se sono corretti)
    elif key == 13:
      if checkVertices(state["vertices"]):
        return state["vertices"]
      else:
        state["vertices"] = []
    # se è stato premuto esc o la q, il programma viene terminato
    elif key == 27 or key == ord("q"):
      return


# ======================= PERSPECTIVE TRANSFORM ======================
# funzione per effettuare una trasformazione prospettica partendo da un frame e 4 punti su di esso
def perspectiveTransform(frame, face):
  if(len(face) != 4):
    return None
  
  pts = np.float32([(0, 0), (400, 0), (400, 400), (0, 400)])
  matrix = cv.getPerspectiveTransform(np.float32([face]), pts)
  result = cv.warpPerspective(frame, matrix, (400, 400))
  return result


# ============================ FIND FACES ============================
# funzione per identificare le facce del cubo dati 7 vertici
def findFaces(vertices, cameraPosition):
  # calcolo l'inviluppo convesso dei vertici
  convexHull = cv.convexHull(np.array(vertices), True)
  # converto convexHull in un array di tuple
  convexHull = [tuple(point[0]) for point in convexHull]

  # se i punti nell'inviluppo non sono 6, significa che i vertici non appartengono ad un cubo, perciò ritorna liste vuote 
  if(len(convexHull) != 6):
    return [], [], []

  # trovo il vertice comune alle tre facce, sapendo che è l'unico a non fa parte dell'inviluppo convesso
  mainVertex = None
  for vertex in vertices:
    if vertex not in convexHull:
      mainVertex = vertex

  # riordino i punti dell'inviluppo convesso in base alla posizione della camera
  # prestare attenzione all'ordine dei punti negli array delle facce (face1, face2, face3), perchè indicherà l'orientamento della faccia
  if cameraPosition == 0:
    # camera posta sopra al cubo, riordino in senso antiorario
    convexHull = sortPoints(convexHull, clockwise = False)
    # up face
    face1 = [convexHull[1], convexHull[0], convexHull[5], mainVertex]
    # left face
    face2 = [convexHull[1], mainVertex, convexHull[3], convexHull[2]]
    # front face
    face3 = [mainVertex, convexHull[5], convexHull[4], convexHull[3]]
  elif cameraPosition == 1:
    # camera posta sotto al cubo, riordino in senso orario
    convexHull = sortPoints(convexHull, clockwise = True)
    # right face
    face1 = [convexHull[5], convexHull[0], mainVertex, convexHull[4]]
    # back face
    face2 = [convexHull[0], convexHull[1], convexHull[2], mainVertex]
    # down face
    face3 = [convexHull[3], convexHull[4], mainVertex, convexHull[2]]

  return face1, face2, face3


# =========================== FIND FACELET ===========================
# funzione per identificare le 9 facelet data una faccia (ovvero un array di 4 vertici)
def findFacelet(face):
  # cerco il vertice con coordinata y minore
  minY = min(face, key=lambda vertex: vertex[1])

  edge1 = (face[0], face[1])
  edge2 = (face[1], face[2])
  edge3 = [face[2], face[3]]
  edge4 = [face[3], face[0]]
  edges = [edge1, edge2, edge3, edge4]

  # matrice in cui ogni elemento rappresenta le coordinate di un vertice di una facelet
  # +----+----+----+----+
  # |  0 |  1 |  2 |  3 |
  # +----+----+----+----+
  # |  4 |  5 |  6 |  7 |
  # +----+----+----+----+
  # |  8 |  9 | 10 | 11 |
  # +----+----+----+----+
  # | 12 | 13 | 14 | 15 |
  # +----+----+----+----+
  # inizializzo la matrice con coordinate (0, 0)
  faceletPoints = [[(0, 0) for _ in range(4)] for _ in range(4)]

  # aggiungo alla matrice le coordinate dei 4 punti che dividono ogni spigolo
  for i, edge in enumerate(edges):
    p1 = edge[0]
    p4 = edge[1]
    x1 = p1[0] + (p4[0] - p1[0]) / 3
    y1 = p1[1] + (p4[1] - p1[1]) / 3
    p2 = (int(x1), int(y1))
    x2 = p1[0] + 2 * (p4[0] - p1[0]) / 3
    y2 = p1[1] + 2 * (p4[1] - p1[1]) / 3
    p3 = (int(x2), int(y2))

    if i == 0:
      faceletPoints[0][0] = p1
      faceletPoints[0][1] = p2
      faceletPoints[0][2] = p3
    elif i == 1:
      faceletPoints[0][3] = p1
      faceletPoints[1][3] = p2
      faceletPoints[2][3] = p3
    elif i == 2:
      faceletPoints[3][3] = p1
      faceletPoints[3][2] = p2
      faceletPoints[3][1] = p3
    elif i == 3:
      faceletPoints[3][0] = p1
      faceletPoints[2][0] = p2
      faceletPoints[1][0] = p3

  # aggiungo alla matrice le coordinate dei 4 punti della facelet centrale
  # essi sono ottenuti dalle intersezioni dei segmenti che congiungono i punti intermedi degli spigoli opposti
  p1 = intersect((faceletPoints[0][1], faceletPoints[3][1]), (faceletPoints[1][0], faceletPoints[1][3]))
  p2 = intersect((faceletPoints[0][2], faceletPoints[3][2]), (faceletPoints[1][0], faceletPoints[1][3]))
  p3 = intersect((faceletPoints[0][1], faceletPoints[3][1]), (faceletPoints[2][0], faceletPoints[2][3]))
  p4 = intersect((faceletPoints[0][2], faceletPoints[3][2]), (faceletPoints[2][0], faceletPoints[2][3]))
  faceletPoints[1][1] = tuple(int(value) for value in p1)
  faceletPoints[1][2] = tuple(int(value) for value in p2)
  faceletPoints[2][1] = tuple(int(value) for value in p3)
  faceletPoints[2][2] = tuple(int(value) for value in p4)

  # converto la matrice in 9 array che contengono ciascuno i 4 punti di ogni facelet
  facelet = []
  for row in range(len(faceletPoints) - 1):
    for column in range(len(faceletPoints[row]) - 1):
      a = faceletPoints[row][column]
      b = faceletPoints[row][column+1]
      c = faceletPoints[row+1][column+1]
      d = faceletPoints[row+1][column]
      facelet.append([a, b, c, d])

  return facelet


# =========================== SCAN COLORS ============================
# funzione per trovare la media dei colori dei pixel di ciascuna facelet
def scanColors(frame, faces):
  face1, face2, face3 = faces

  # controllo che le facce abbiano 4 vertici
  if len(face1) != 4 and len(face2) != 4 and len(face3) != 4:
    return [], [], []

  # effettuo la trasformazione della prospettiva, ottenendo un frame di ogni faccia vista frontalmente
  face1Frame = perspectiveTransform(frame, face1) # upper/right face
  face2Frame = perspectiveTransform(frame, face2) # left/back face
  face3Frame = perspectiveTransform(frame, face3) # front/down face

  # trovo i vertici delle 9 facelet, che sono uguali per tutte le 3 facce (essendo ogni faccia vista frontalmente)
  facelet = findFacelet([(0, 0), (400, 0), (400, 400), (0, 400)])
  face1Colors = []
  face2Colors = []
  face3Colors = []

  for f in facelet:
    # offset in px della roi (region of interest) rispetto alla facelet, in modo da evitare errori nella rilevazione del colore
    offset = 30
    x1 = f[0][0] + offset
    x2 = f[1][0] - offset
    y1 = f[0][1] + offset
    y2 = f[3][1] - offset
    # calcolo le roi, che corrispondono alle facelet delle 3 facce
    roiFace1 = face1Frame[y1:y2, x1:x2]
    roiFace2 = face2Frame[y1:y2, x1:x2]
    roiFace3 = face3Frame[y1:y2, x1:x2]
    # calcolo la media bgr di ogni roi
    roiFace1Average = averageColor(roiFace1)
    roiFace2Average = averageColor(roiFace2)
    roiFace3Average = averageColor(roiFace3)
    # converto le medie bgr in int
    roiFace1Average = tuple(map(int, roiFace1Average))
    roiFace2Average = tuple(map(int, roiFace2Average))
    roiFace3Average = tuple(map(int, roiFace3Average))
    # aggiungo le medie rgb ai corrispettivi array
    face1Colors.append(roiFace1Average)
    face2Colors.append(roiFace2Average)
    face3Colors.append(roiFace3Average)

  return face1Colors, face2Colors, face3Colors


# ============================ SCAN CUBE =============================
# funzione per scansionare il cubo
def scanCube(cameraType):
  # carico le facce del cubo dai file json, creati tramite config.py
  faces0 = loadFaces("cam0.json")
  faces1 = loadFaces("cam1.json")

  # inizializzo camera0 e camera1 in base al loro tipo (raspi o system)
  camera0 = getCamera(cameraType, 0)
  camera1 = getCamera(cameraType, 1)

  # catturo un frame di ognuna delle 2 camere
  frame0 = getFrame(camera0)
  frame1 = getFrame(camera1)

  # rilascio le risorse
  if cameraType == "raspi":
    camera0.stop()
    camera1.stop()
  elif cameraType == "system":
    camera0.release()
    camera1.release()
    
  # escludo le braccia di aggacio dai frame
  frame0 = maskArms(frame0)
  frame1 = maskArms(frame1)

  # scansiono il cubo, trovando i colori rgb di ogni facelet
  upperColors, leftColors, frontColors = scanColors(frame0, faces0)
  rightColors, backColors, downColors = scanColors(frame1, faces1)

  # converto gli rgb delle facelet in un json
  json = facesColorsToJson(upperColors, leftColors, frontColors, rightColors, backColors, downColors)

  scan_data = eval(json)
  for key, value in scan_data.items():
    # converto il valore bgr in rgb
    value = convertRgbBgr(value)
    scan_data[key] = tuple(value)
  
  # identifico il colore di ciascuna facelet, partendo dagli rgb
  cube = RubiksColorSolverGeneric(3)
  cube.enter_scan_data(scan_data)
  cube.crunch_colors()
  cube.print_cube()
  cubeString = "".join(cube.cube_for_kociemba_strict())
  
  return cubeString


# ============================ SOLVE CUBE ============================
# funzione per risolvere il cubo
def solveCube(cubeString):
  # trovo la stringa di risoluzione del cubo
  resolution = solver.solve(cubeString, 0, 0.2)
  
  # controllo che non ci siano stati errori nella risoluzione
  if "error" not in resolution.lower():
    # rimuovo dalla stringa di risoluzione i caratteri non necessari
    resolution = resolution.replace(" ", "")
    index = resolution.find("(")
    resolution = resolution[:index]
    
  return resolution