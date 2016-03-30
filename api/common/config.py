import os
from api.__init__ import parentdir

db_file = 'db.sqlite'

db_dir = os.path.join(parentdir, 'store', db_file)

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(db_dir)
JSONIFY_PRETTYPRINT_REGULAR = True
JSON_AS_ASCII = False
