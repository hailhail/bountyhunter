from bountyhunter import app
from bountyhunter import db
from bountyhunter import models
from flask import render_template
from sqlalchemy import and_

@app.route('/')
def index():
    requests = models.Request.query \
                     .filter(and_(models.Request.bandcamp != '', models.Request.cost != None)) \
                     .filter(models.Request.cost != 0.0) \
                     .all()
    return render_template('index.html', requests=requests)
