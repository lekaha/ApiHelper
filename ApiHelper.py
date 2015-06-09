#!/usr/bin/python
# -*- coding: utf-8 -*-

class ApiHelper:
    """ Api Helper """

    def __init__(self, auth):
        self.mAuth = auth

    def verify():
        if None != auth:
            return True
        return False

    def call(self, caller, handle, callback):
        r = caller.call(handle)
        if r != None:
            return callback(r)

class Authentication:
    pass

class Caller:
    pass

class HttpCaller(Caller):
    UserAgent = 'Application'
    def call(self, handle):
        if isinstance(handle, HttpRequestHandle):
            import urllib
            import urllib2
            import json

            method = handle.method
            url = handle.url
            paras = urllib.urlencode(handle.parameters)
            headers = handle.headers
            r = None
            if None != headers:
                if handle.method == "GET":
                    r = urllib2.urlopen(urllib2.Request(url + "?" + paras, None, headers))
                else:
                    r = urllib2.urlopen(urllib2.Request(url, paras, headers))
            else:
                if handle.method == "GET":
                    r = urllib2.urlopen(urllib2.Request(url + "?" + paras, None, { \
                        'User-Agent': self.UserAgent}))
                else:
                    r = urllib2.urlopen(urllib2.Request(url, paras, { \
                        'User-Agent': self.UserAgent}))
            return json.load(r)

class Handle:
    pass

class HttpRequestHandle:

    def __init__(self, method = "GET"):
        self.method = method
        self.headers = None
        self.url = None
        self.parameters = None

    def setUrl(self, url):
        self.url = url
        return self

    def setParameters(self, paras):
        self.parameters = paras
        return self

    def setHeader(self, headers):
        self.headers = headers
        return self

def callback(response):
    pass

if __name__ == '__main__':
    auth = Authentication()
    api = ApiHelper(auth)

    handle = HttpRequestHandle().setUrl("").setParameters("").setHeader("")
    api.call(HttpCaller(), handle, callback)


