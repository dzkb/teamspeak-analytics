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

# TeamSpeak 3 serverquery module

import telnetlib

class TeamSpeak:

    def __init__(self, host, port):
        self.tn = telnetlib.Telnet(host, port)

        message = self.tn.read_until(b"\n") # check if connected 
        assert(message == b"TS3\n")
        self.tn.read_until(b"\n")

    def authenticate(self, login, password):
        payload = "login {0} {1}\n".format(login, password).encode("ascii") # try to log in
        self.tn.write(payload)

        message = self.tn.read_until(b"\n") # check if logged in
        assert(b"msg=ok" in message)

    def select_server(self, sid):
        payload = "use {0}\n".format(sid).encode("ascii") # select server
        self.tn.write(payload)

        message = self.tn.read_until(b"\n") # check if success
        assert(b"msg=ok" in message)

    def query(self, query):
        query = query + b"\n"
        self.tn.write(query)
        reply_data = self.tn.read_until(b"\n").rstrip(b"\n").strip(b"\r") # read list

        message = self.tn.read_until(b"\n") # read reply code
        assert(b"msg=ok" in message)
        return reply_data

class QueryParser:
    # generates list of dictionaries describing teamspeak objects
    # from serverquery returned string

    def parse(self, data):
        output = []

        raw_objects = data.split(b"|") # Pipe delimits objects

        for raw_obj in raw_objects:
            final_obj = {} # create dictionary describing object

            object_data = raw_obj.split(b" ") # space delimits key=value

            for keyval in object_data:
                keyval_list = keyval.split(b"=") # equality sing separates key from value

                final_obj[keyval_list[0].decode("utf-8")] = keyval_list[1].decode("utf-8")

            output.append(final_obj)

        return output
