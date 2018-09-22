# GEOWALL CONFIGURATION FILE
# ---------------------------
import sys
import os

# local folder path
loc = os.path.dirname(os.path.abspath(__file__))

# database location
TINY_DB = loc + 'geowall.json'

# revealjs folders
REVEAL_HTML_DIR = loc + '/src_html/'
REVEAL_TEMPL_DIR = loc + '/data/templates/'
REVEAL_PATH = loc + "/revealjs/reveal.js/"

# name of basic presentations

PROJECT_INFO_TEMPL = "goals.html"
PROJECT_IMPACTS_TEMPL = "impacts.html"
PROJECT_IMG_TEMPL = "images.html"
PROJECT_DISC_TEMPL = "disciplines.html"

# server paths
REVEAL_URL = "http://localhost:8080/revealjs/"
WS_URL = 'ws://localhost:8080/GeoWallWebSocket'
