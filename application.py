#used for Report process Funtion

from flask import Flask

UPLOAD_FOLDER = (r'/data/PROJECTS/NOC_OPTICS_TAC3_Project/rawdata/inventory/')

application = Flask(__name__)
application.secret_key = "secret key"
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

