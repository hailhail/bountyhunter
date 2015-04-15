import re
import whatapi

from bountyhunter import db
from bountyhunter import models

def bandcamp_match(description):
    """
    Regular expression search for bandcamp requests

    :type description: string
    :params description: description of W.CD request

    """

    match = re.search('https?://.*\.bandcamp\.com/?(?:[a-zA-Z]+)?/[\w-]*', description.lower())
    if match:
        return match.group()
    return None

requests = models.Request.query.all()

uids = list()

for request in requests:
    bandcamp = bandcamp_match(request.description)
    if bandcamp:
        uids.append(request.id)

for uid in uids:
    print uid
    request = models.Request.query.filter_by(id=uid).first()
    request.bandcamp = bandcamp_match(request.description)
    db.session.commit()
