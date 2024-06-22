# ============================ LIBRARIES =============================
import utils
import argparse


# =============================== MAIN ===============================
def main():
  # analizzo gli argomenti passati come parametri
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--type", help = "type of camera (system or raspi)", choices=["system", "raspi"], default="raspi")
  parser.add_argument("-c", "--camera", help = "camera to use (0 or 1)", type=int, choices=[0, 1], default=0)
  parser.add_argument("-p", "--position", help = "position of the camera (0=up or 1=down)", type=int, choices=[0, 1])
  args = parser.parse_args()
  cameraType = args.type
  cameraNumber = args.camera
  cameraPosition = args.position if args.position else cameraNumber

  # inizializzo l'oggetto camera in base al tipo (system o raspi)
  camera = utils.getCamera(cameraType, cameraNumber)

  # seleziono manualmente i vertici
  vertices = utils.selectVertices(camera, cameraPosition)
  
  if vertices == None:
    return

  # trovo i vertici di ciascuna faccia
  face1, face2, face3 = utils.findFaces(vertices, cameraPosition)
  
  # salvo le facce in un json
  utils.saveFaces([face1, face2, face3], f"cam{cameraPosition}.json")
  print("Faces saved successfully")

  # rilascio le risorse
  if cameraType == "raspi":
    camera.stop()
  elif cameraType == "system":
    camera.release()


if __name__ == "__main__":
  main()