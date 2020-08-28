import os
import glob
import shutil
import socket
import subprocess
import requests, json
import random
from flask_cors import CORS
from flask import Flask, request, render_template
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST","GET"])
# @app.route("/json-gui", endpoint="gui", methods=["POST","GET"])

def jsontask():
    # Current working directory
    cwd = os.getcwd()
    # POST
    if request.method == "POST":
        os.chdir(cwd)

        # Going to add a randomly named the temp_folder - avoiding any naming conflicts
        temp_folder = str(random.randint(1000000000,9999999999))
        os.makedirs(temp_folder)

        # Take the posted json data
        req = request.get_json()

        # {
        #     "datafile": "...",
        #     "data": "...",
        #     "codefile": "...",
        #     "code": "..."
        # }

        # Get data and temporarily save as file
        datafile = req["datafile"]
        data = req["data"]
        if not datafile == "":
            df = open("{}/{}".format(temp_folder, datafile), "w+")
            df.write(data)
            df.close()

        # Get code and temporarily save as file
        codefile = req["codefile"]
        code = req["code"]
        # code = "print('hello wtf')"
        if codefile.endswith(".py") and len(codefile) > 3:
            cf = open("{}/{}".format(temp_folder, codefile), "w+")
            cf.write(code)
            cf.close()
        else:
            # Remove temp_folder
            shutil.rmtree(temp_folder)
            return jsonify(
                output="Please enter a proper code filename ending with '.py'"
            )

        # Enter temp_files directory and execute code file
        os.chdir(temp_folder)
        
        # Try to run the code with subprocess (python3)
        try:
            process = subprocess.check_output(
                ["python3", codefile],
                stderr=subprocess.STDOUT,
                universal_newlines=True)
        # Check for error message
        except subprocess.CalledProcessError as e:
            # Leave temp_folder
            os.chdir(cwd)

            # Remove temp_folder
            shutil.rmtree(temp_folder)
            
            return jsonify(
                output=e.output
            )

        else:
            # If run successfully

            # Leave temp_folder
            os.chdir(cwd)

            # Remove temp_folder
            shutil.rmtree(temp_folder)

            return jsonify(
                output=process.rstrip(),
            )

    # GET
    else:
        os.chdir(cwd)
        return render_template("json-task.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000, debug=True)
