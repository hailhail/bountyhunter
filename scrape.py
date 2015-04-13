#!/usr/bin/env python

import ConfigParser
import re
import time
import whatapi

from bountyhunter import db
from bountyhunter import models
from datetime import datetime

def retrieve_page(handle, page_num, show_filled):
    show_filled = 'false' if False else 'true'

    try:
        r = handle.request('requests', page=page_num, show_filled=show_filled)
        return r['response']['results']
    except:
        return list()

def retrieve_pages(handle, show_filled=False):
    start_page = 1
    index = retrieve_total(handle, show_filled=show_filled)
    print 'Total pages: %i' % index

    while (index >= start_page):
        print 'Scrape page=%i' % index
        results = retrieve_page(handle, page_num=index, show_filled=show_filled)
        if len(results) > 0:
            temp = dict()
            for result in results:
                request = models.Request(id=result['requestId'],
                         bounty=result['bounty'],
                         description=result['description'],
                         isFilled=result['isFilled'],
                         lastVote=to_date(result['lastVote']),
                         timeAdded=to_date(result['timeAdded']),
                         voteCount=result['voteCount'],
                         year=result['year'])
                temp[result['requestId']] = request
            for each in models.Request.query.filter(models.Request.id.in_(temp.keys())).all():
                db.session.merge(temp.pop(each.id))
            db.session.add_all(temp.values())
            db.session.commit()
        index -= 1
        time.sleep(3)

def retrieve_total(handle, show_filled):
    try:
        r = handle.request('requests', page=1, show_filled=show_filled)
        return int(r['response']['pages'])
    except:
        return 0

def to_date(dt):
    match = re.match(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})', dt)
    d = match.groupdict()
    return datetime(year=int(d['year']),
                    month=int(d['month']),
                    day=int(d['day']),
                    hour=int(d['hour']),
                    minute=int(d['min']),
                    second=int(d['sec'])
                    )

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('account.ini')

    try:
        apihandle = whatapi.WhatAPI(username=config.get('Account', 'Username'), password=config.get('Account', 'Password'))
        print 'Authentication success!'
    except:
        print 'Authentication failure! Ensure correct login information in account.ini'

    retrieve_pages(apihandle)
