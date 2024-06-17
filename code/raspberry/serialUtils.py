# ============================ LIBRARIES =============================
import serial
from gpiozero import DigitalOutputDevice
import pyduinocli
import time


# ========================== CONFIGURATION ===========================
PORT = "/dev/ttyAMA0"
BAUDRATE = 9600
FQBN = "arduino:avr:mega"
RESET = 4


# ============================== WRITE ===============================
def write(string):
  arduino = serial.Serial(PORT, baudrate=BAUDRATE, timeout=0)
  time.sleep(0.5)
  arduino.write(str.encode(string))
  arduino.close() 


# =============================== READ ===============================
def read():
  arduino = serial.Serial(PORT, baudrate=BAUDRATE, timeout=0)
  response = arduino.readline()
  return response


# ========================== COMPILE SKETCH ==========================
def compileSketch(path):
  arduino = pyduinocli.Arduino()
  arduino.compile(fqbn=FQBN, sketch=path)
  

# ========================== UPLOAD SKETCH ===========================
# funzione per impostare l'arduino in modalità bootloader e caricare uno sketch
def uploadSketch(path):
  arduino = pyduinocli.Arduino()
  reset = DigitalOutputDevice(RESET)
  reset.off()
  time.sleep(0.1)
  reset.on()
  arduino.upload(fqbn=FQBN, sketch=path, port=PORT)
