from flask import Flask

# -------- Global initializations ----------
flask = Flask(__name__)

# ----- Load the routes ----
import api.routes
