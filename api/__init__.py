from flask import Flask

# -------- Global initializations ----------
flask = Flask(__name__)
flask.config.from_object('api.settings')

# ----- Load the routes ----

import api.routes
