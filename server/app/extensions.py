from flask_cors import CORS

import log

cors = CORS()
logger = log.get_logger(__name__)
