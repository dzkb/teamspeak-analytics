'''
Copyright (c) 2016 Dzakub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from teamspeak import *
import pprint
import sqlite3
import time
import json
from couchbase.bucket import Bucket

CURRENT_TIMESTAMP = int(time.time())

cfg = open("ts_config.cfg", "r") # parse config
records = {}
for line in cfg:
    record = line.rstrip("\n").split("=")
    records[record[0]] = record[1]

teamspeak = TeamSpeak(records["host"], records["port"])
parser = QueryParser()
teamspeak.authenticate(records["username"], records["password"])
teamspeak.select_server(records["serverid"])

channels = parser.parse(teamspeak.query(b"channellist"))
clients = parser.parse(teamspeak.query(b"clientlist"))

output_data = {"channels" : channels, "clients" : clients}

bucket = Bucket("couchbase://localhost/default")
# print(json.dumps(output_data))

bucket.insert(str(int(time.time())), output_data)

# reply_data = parser.parse(teamspeak.query(b"clientlist"))
# reply_data = parser.parse(teamspeak.query(b"channellist"))

# pprint.pprint(reply_data)

# raw_users = reply_data.split(b"|")

# visited_channels = set()

# for data in raw_users:
#     userdata = data.split(b" ")
#     for client_data in userdata:
#         if b"cid=" in client_data:
#             channel_id = client_data.split(b"=")[1]
#             visited_channels.add(channel_id)

# pprint.pprint(visited_channels, width=1)

