import os
import glob
import socket
import subprocess
import requests, json
import random
from flask_cors import CORS
from flask import Flask, request, render_template
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route("/json-task", endpoint="task", methods=["POST","GET"])
@app.route("/json-gui", endpoint="gui", methods=["POST","GET"])
def jsontask():
    # POST
    if request.method == "POST":
        if not os.path.exists("temp_files"):
            os.makedirs("temp_files")

        # Going to add a random number for filenames - avoiding any conflicts
        # temp_id = random.randint(1000000,2000000)

        # Get data and temporarily save as file
        d_name = request.form["d_name"]
        data = request.form["data"]
        if not d_name == "":
            df = open("temp_files/{}".format(d_name), "w+")
            df.write(data)
            df.close()

        # Get code and temporarily save as file
        c_name = request.form["c_name"]
        code = request.form["code"]
        if c_name.endswith(".py") and len(c_name) > 3:
            cf = open("temp_files/{}".format(c_name), "w+")
            cf.write(code)
            cf.close()
        else:
            return render_template("json-task.html",
                output="Please enter a proper code filename ending with '.py'",
                d_name=d_name,
                data=data,
                c_name=c_name,
                code=code)

        # Enter temp_files directory and execute code file
        os.chdir("temp_files")
        
        # Try to run the code with subprocess (python3)
        try:
            process = subprocess.check_output(
                ["python3", c_name],
                stderr=subprocess.STDOUT,
                universal_newlines=True)
        # Check for error message
        except subprocess.CalledProcessError as e:
            # Leave temp_files directory
            os.chdir("..")
            if request.endpoint == "gui": 
                # Return error message
                return render_template("json-task.html",
                    output=e.output,
                    d_name=d_name,
                    data=data,
                    c_name=c_name,
                    code=code)
            else:
                return jsonify(
                    output=e.output
                )
        else:
            # If run successfully, delete the temporarily saved files
            files = glob.glob("*")
            for f in files:
                os.remove(f)
            # Leave temp_files directory
            os.chdir("..")
            if request.endpoint == "gui":
                # Return output
                return render_template("json-task.html",
                    output=process,
                    d_name=d_name,
                    data=data,
                    c_name=c_name,
                    code=code)
            else:
                return jsonify(
                    output=process
                )
    # GET
    else:
        #return "{}".format(request.endpoint)
        return render_template("json-task.html", endpoint=request.endpoint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
