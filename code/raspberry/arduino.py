import serialUtils
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", help = "path of the sketch to upload to Arduino")
  args = parser.parse_args()
  path = args.path
  
  serialUtils.compileSketch(path)
  print("Compiled")
  serialUtils.uploadSketch(path)
  print("Uploaded")


if __name__ == "__main__":
  main()