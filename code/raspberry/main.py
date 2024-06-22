# ============================ LIBRARIES =============================
import utils
import serialUtils
import argparse


# =============================== MAIN ===============================
def main():
  # analizzo gli argomenti passati come parametri
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--type", help = "type of camera (system or raspi)", choices=["system", "raspi"], default="raspi")
  args = parser.parse_args()
  cameraType = args.type
  
  cubeString = utils.scanCube(cameraType)
  resolution = utils.solveCube(cubeString)
  serialUtils.write(resolution)


if __name__ == "__main__":
  main()