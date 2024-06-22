# ============================ LIBRARIES =============================
import utils
from rubikscolorresolver.solver import RubiksColorSolverGeneric
import twophase.solver as solver


# =============================== MAIN ===============================
def main():
  # inizializzo l'oggetto camera in base al tipo (system o raspi)
  cameraType = "system"
  cameraNumber = 0
  camera = utils.getCamera(cameraType, cameraNumber)
  
  cameraPosition = 0
  # seleziono manualmente i vertici della cam0
  vertices1 = utils.selectVertices(camera, cameraPosition)
  # trovo i vertici delle 3 facce
  upperFace, leftFace, frontFace = utils.findFaces(vertices1, cameraPosition)
  # catturo un frame
  frame = utils.getFrame(camera)
  # escludo le braccia di aggacio dal frame
  frame = utils.maskArms(frame)
  # scansiono il cubo, trovando i colori rgb di ogni facelet
  upperColors, leftColors, frontColors = utils.scanColors(frame, (upperFace, leftFace, frontFace))
  
  cameraPosition = 1
  # seleziono manualmente i vertici della cam1
  vertices2 = utils.selectVertices(camera, cameraPosition)
  # trovo i vertici delle 3 facce
  rightFace, backFace, downFace = utils.findFaces(vertices2, cameraPosition)
  # catturo un frame
  frame = utils.getFrame(camera)
  # escludo le braccia di aggacio dal frame
  frame = utils.maskArms(frame)
  # scansiono il cubo, trovando i colori rgb di ogni facelet
  rightColors, backColors, downColors = utils.scanColors(frame, (rightFace, backFace, downFace))

  # converto gli rgb delle facelet in un json
  json = utils.facesColorsToJson(upperColors, leftColors, frontColors, rightColors, backColors, downColors)

  scan_data = eval(json)
  for key, value in scan_data.items():
    # converto il valore bgr in rgb
    value = utils.convertRgbBgr(value)
    scan_data[key] = tuple(value)

  # identifico il colore di ciascuna facelet, partendo dagli rgb
  cube = RubiksColorSolverGeneric(3)
  cube.enter_scan_data(scan_data)
  cube.crunch_colors()
  cube.print_cube()
  cubeString = "".join(cube.cube_for_kociemba_strict())

  # trovo la stringa di risoluzione del cubo
  resolution = solver.solve(cubeString, 0, 0.2)
  print(resolution)


if __name__ == "__main__":
  main()
