# ============================ LIBRARIES =============================
import utils
import argparse
import cv2 as cv
from rubikscolorresolver.solver import RubiksColorSolverGeneric
import twophase.solver as solver


# =============================== MAIN ===============================
def main():
  # analizzo gli argomenti passati come parametri
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--type", help = "type of camera (system or raspi)", choices=["system", "raspi"], default="raspi")
  args = parser.parse_args()
  cameraType = args.type
  
  # carico le facce del cubo dai file json, creati tramite il config.py
  faces0 = utils.loadFaces("cam0.json")
  faces1 = utils.loadFaces("cam1.json")

  # inizializzo camera0 e camera1 in base al loro tipo (system o raspi)
  camera0 = utils.getCamera(cameraType, 0)
  camera1 = utils.getCamera(cameraType, 1)

  # catturo un frame di ognuna delle 2 camere
  frame0 = utils.getFrame(camera0)
  frame1 = utils.getFrame(camera1)
  
  # ruoto di 180 gradi il frame della camera superiore
  frame0 = cv.rotate(frame0, cv.ROTATE_180)

  # rilascio le risorse
  if cameraType == "raspi":
    camera0.stop()
    camera1.stop()
  elif cameraType == "system":
    camera0.release()
    camera1.release()
    
  # escludo le braccia di aggacio dai frame
  frame0 = utils.maskArms(frame0)
  frame1 = utils.maskArms(frame1)

  # scansiono il cubo, trovando i colori rgb di ogni facelet
  upperColors, leftColors, frontColors = utils.scanCube(frame0, faces0)
  rightColors, backColors, downColors = utils.scanCube(frame1, faces1)

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