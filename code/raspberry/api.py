import utils
import serialUtils
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api", methods=["GET", "POST"])
def index():
  if request.method == "GET":
    action = request.args.get('action')

    if action == "solve":
      cubeString = utils.scanCube("raspi")
      resolution = utils.solveCube(cubeString)
      serialUtils.write(resolution)
      return jsonify({"message": "Solved"})
    
    elif action == "move":
      movements = request.args.get('movements')
      if len(movements) > 0:
        serialUtils.write(movements)
        return jsonify({"message": f"{movements}"}), 200
      
    return jsonify({"message": "Connected"}), 200


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=6001)