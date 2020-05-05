import settings
from flask import Flask
from jobs import job
import models

app = Flask(__name__)
app.config.from_object(settings.BaseConfig)
models.init_db(app)
app.cli.add_command(job)
