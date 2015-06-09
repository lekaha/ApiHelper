#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import ApiHelper

API_POST_ACCESS_TOKEN = "https://typetalk.in/oauth2/access_token"
API_POST_MESSAGE = "https://typetalk.in/api/v1/topics/{id}"
API_GET_MESSAGE = "https://typetalk.in/api/v1/topics/{id}"

class TypetalkApiHelper(ApiHelper.ApiHelper):

    def AuthCallback(self, response):
        self.token = response['access_token']

    def verify(self, scope):
        self.token = None
        url = API_POST_ACCESS_TOKEN
        paras = {"client_id": self.mAuth.key, \
            "client_secret": self.mAuth.secret, \
            "grant_type": "client_credentials", \
            "scope": scope}
        handle = ApiHelper.HttpRequestHandle("POST") \
            .setUrl(url) \
            .setParameters(paras)
        self.call(ApiHelper.HttpCaller(), handle, self.AuthCallback)

        if None != self.token:
            print "Access Token = ", self.getToken()
            return True
        return False

    def getToken(self):
        return self.token

class TypetalkAuthentication(ApiHelper.Authentication):
    def __init__(self, key = "", secret = ""):
        self.key = key
        self.secret = secret

    def setKey(self, key):
        self.key = key

    def setSecret(self, secret):
        self.secret = secret

def Callback(response):
    return response

def Callback2(response, regx):
    import re
    for i in response:
        if None != regx:
            m = re.search(regx, i['message'])
            if None != m:
                print m.group(0)
                return True
        else:
            print "No regx ", i['message']

    return False

def sendMessage(helper, id, msg):
    scope = "topic.post"
    if helper.verify("topic.post"):
        auth = "Bearer %s" % helper.getToken()
        url = API_POST_MESSAGE.format(id = id)
        handle = ApiHelper.HttpRequestHandle("POST") \
            .setUrl(url) \
            .setParameters({"message": msg}) \
            .setHeader({"Authorization": auth})
        helper.call(ApiHelper.HttpCaller(), handle, lambda r: Callback(r))
        return True
    return False

def receiveMessage(helper, id, regx = None):
    scope = "topic.read"
    if helper.verify(scope):
        auth = "Bearer %s" % helper.getToken()
        url = API_GET_MESSAGE.format(id = id)
        handle = ApiHelper.HttpRequestHandle() \
            .setUrl(url) \
            .setParameters({"count": "10"}) \
            .setHeader({"Authorization": auth})
        return helper.call(ApiHelper.HttpCaller(), handle, lambda r: Callback2(r['posts'], regx))

if __name__ == "__main__":
    if (None != sys.argv) and len(sys.argv) > 2:
        KEY = sys.argv[1]
        SECRET = sys.argv[2]
        auth = TypetalkAuthentication(KEY, SECRET)
        helper = TypetalkApiHelper(auth)

        result = sendMessage(helper, "9495", "test")
        if not result:
            print "Send message fail"

        result = receiveMessage(helper, "13575", '(?<=Bye )john')
        if result:
            print "Got it"
        else:
            print "No...."
    else:
        print "Pls give Key and Secret."
