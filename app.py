from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys

app = Flask(__name__)



# app.py code



if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern
    print("Bjoern is running.")
    bjoern.run(app, "0.0.0.0", 5016)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    print("Running in testing mode!")
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()
