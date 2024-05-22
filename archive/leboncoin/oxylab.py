import urllib.request
import random

username = "safeflat"
password = "pJbY6KrL7NswfXt"
entry = "http://customer-%s:%s@pr.oxylabs.io:7777" % (username, password)
query = urllib.request.ProxyHandler(
    {
        "http": entry,
        "https": entry,
    }
)
execute = urllib.request.build_opener(query)
print(execute.open("https://www.seloger.com/").read())
