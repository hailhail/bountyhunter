#!/usr/bin/env python

import ConfigParser
import re
import requests
import time
import whatapi

from bountyhunter import db
from bountyhunter import models
from bs4 import BeautifulSoup
from datetime import datetime

def bandcamp_match(description):
    """
    Regular expression search for bandcamp requests

    :type description: string
    :params description: description of W.CD request

    """

    match = re.search('https?://.*\.bandcamp\.com/?(?:[a-zA-Z]+)?/[\w-]*', description.lower())
    if match:
        return match.group()
    return ''

def extract_currency(s):
    match = re.search(r'\d+(?:.\d+)?', s)
    if match:
        return match.group()
    return 0.0

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
                bandcamp = bandcamp_match(result['description'])
                cost = scrape_bandcamp(bandcamp) if bandcamp else 0.0

                request = models.Request(id=result['requestId'],
                         bandcamp=bandcamp,
                         bounty=result['bounty'],
                         cost=cost,
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

def scrape_bandcamp(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        span = soup.find('span', class_='base-text-color')
        if span:
            cost = extract_currency(span.contents[0])
            if cost:
                print 'bandcamp: %0.2f' % float(cost)
                return float(cost)
    except:
        return 0.0

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
