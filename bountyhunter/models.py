from bountyhunter import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bounty = db.Column(db.Integer)
    cost = db.Column(db.Float)
    description = db.Column(db.Text)
    isFilled = db.Column(db.Boolean)
    lastVote = db.Column(db.DateTime)
    timeAdded = db.Column(db.DateTime)
    url = db.Column(db.Text)
    voteCount = db.Column(db.Integer)
    year = db.Column(db.Integer)
    bandcamp = db.Column(db.Text)

    def __repr__(self):
        return '<Request %i>' % (self.id)
