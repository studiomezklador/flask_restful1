import os
from bootstrap import app

db_file = 'main.sqlite'
# db_dir = os.path.join(parentdir, 'store', db_file)
db_dir = os.path.join(app.root_path, 'store', db_file)


SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(db_dir)
JSONIFY_PRETTYPRINT_REGULAR = True
JSON_AS_ASCII = False


SECRET_KEY = 'OX8z6c3ULMFgvoH5aVJidqWIunDYx1mrhKpsB7eyCAEZtTSwkQl4PG0fR2jbNOX8z6c3ULMFgvoH5aVJidqWIunDYx1mrhKp'
