# ============================ LIBRARIES =============================
import utils
import rubikscolorresolver.solver as colorSolver
import twophase.solver as solver


# =============================== MAIN ===============================
def main():
  # carico le facce del cubo dai file json, creati tramite il config.py
  faces0 = utils.loadFaces("cam0.json")
  faces1 = utils.loadFaces("cam1.json")

  # inizializzo camera0 e camera1 in base al loro tipo (system o raspi)
  cameraType = "system"
  camera0 = utils.getCamera(cameraType, 0)
  camera1 = utils.getCamera(cameraType, 1)

  # catturo un frame di ognuna delle 2 camere
  frame0 = utils.getFrame(camera0)
  frame1 = utils.getFrame(camera1)

  # rilascio le risorse
  if cameraType == "raspi":
    camera0.stop()
    camera1.stop()
  elif cameraType == "system":
    camera0.release()
    camera1.release()

  # scansiono il cubo, trovando i colori rgb di ogni facelet
  upperColors, leftColors, frontColors = utils.scanCube(frame0, faces0)
  rightColors, backColors, downColors = utils.scanCube(frame1, faces1)

  # converto gli rgb delle facelet in un json
  json = utils.facesColorsToJson(upperColors, leftColors, frontColors, rightColors, backColors, downColors)

  scan_data = eval(json)
  for key, value in scan_data.items():
    scan_data[key] = tuple(value)
  
  # identifico il colore di ciascuna facelet, partendo dagli rgb
  cube = colorSolver(3)
  cube.enter_scan_data(scan_data)
  cube.crunch_colors()
  cube.print_cube()
  cubeString = "".join(cube.cube_for_kociemba_strict())

  # trovo la stringa di risoluzione del cubo
  resolution = solver.solve(cubeString, 0, 0.2)
  print(resolution)


if __name__ == "__main__":
  main()