#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
To use this, go to https://console.cloud.google.com/storage/browser/ka_dev_sync/ (make sure to be logged in as your @ka.org user) and click "snapshot" (it will download the snapshot)
Then move the snapshot (which is probably now ~/Downloads/snapshot) to this directory
'''
import cPickle
import zlib
import base64
import pickle
import io
import datetime

import json
import os
import sys

if not os.path.exists('./snapshot'):
    print 'Snapshot file not found'
    print __doc__
    sys.exit()

print "Loading compressed snapshot"
data = cPickle.load(open('./snapshot'))
print "✅"


def process_items():
    full = []
    print "Uncompressing assessment items"
    for chunk in data['assessment_items']:
        full += cPickle.loads(zlib.decompress(base64.b64decode(chunk)))

    print "Dumping assessment items"
    json.dump(full, open('./assessment_items.json', 'w'), indent=2)
    print "✅"

class FakeObj(object):
    def __init__(self, *args, **kwds):
        self.args = args
        self.kwds = kwds
    def __setstate__(self, state):
        # print type(state)
        if isinstance(state, dict):
            self.__dict__.update(state)
        else:
            self.__dict__.update(state[0])

def as_dict(obj):
    if isinstance(obj, FakeObj):
        return obj.__dict__ # {'args': obj.args, 'kwds': obj.kwds}
    return obj

def back_object(obj):
    if isinstance(obj, FakeObj):
        return back_object(obj.__dict__)
    if isinstance(obj, dict):
        return {k: back_object(v) for k, v in obj.items()}
    if isinstance(obj, tuple) or isinstance(obj, list):
        return [back_object(k) for k in obj]
    return obj

class MyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        try:
            return pickle.Unpickler.find_class(self, module, name)
        except:
            return FakeObj

def process_exs():
    print "Uncompressing exercises"
    raw = zlib.decompress(base64.b64decode(data['frozen_revisions']['Exercise']))
    print "✅"
    file = io.BytesIO(raw)
    print "Processing exercises"
    res = MyUnpickler(file).load()
    good = {}
    for k in res:
        m = back_object(res[k])
        m['creation_date'] = str(m['creation_date'])
        good[k] = m
    print "Dumping exercises"
    json.dump(good, open('./exercises.json', 'wb'), indent=2)
    print "✅"

def process_topics():
    print "Uncompressing topic"
    raw = zlib.decompress(base64.b64decode(data['frozen_revisions']['Topic']))
    print "✅"
    file = io.BytesIO(raw)
    print "Processing topics"
    res = MyUnpickler(file).load()
    good = {}
    for k in res:
        m = back_object(res[k])
        m['creation_date'] = str(m['creation_date'])
        good[k] = m
    print "Dumping topics"
    json.dump(good, open('./topics.json', 'wb'), indent=2)
    print "✅"

# process_items()
# process_exs()
process_topics()
