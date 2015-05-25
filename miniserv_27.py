#! C:\python27\python
from __future__ import print_function

import sys
print("Python version:", sys.version_info[0:3])
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer   import HTTPServer

Handler = SimpleHTTPRequestHandler
Server  = HTTPServer

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000

class MyHandler(SimpleHTTPRequestHandler):

    def __init__(self,req,client_addr,server):
        SimpleHTTPRequestHandler.__init__(self,req,client_addr,server)

    def do_GET(self):
        page_text = "hello<br/>"\
                  + self.server_version +"<br/>"\
                  + self.protocol_version +"<br/>"\
                  + str(self.headers.getheaders('referer')) +"<br/>"\
                  + self.server.client_address +"<br/>"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len( page_text ))
        self.end_headers()
        self.wfile.write( page_text )

server_address   = ('127.0.0.1', port)
httpd = Server(server_address, MyHandler)

try:
    print("httpd.server_name >>>", httpd.server_name)
    print("httpd.server_port >>>", httpd.server_port)
    print("httpd.socket.getsockname() >>>", httpd.socket.getsockname())
    print("Handler.server_version >>>", Handler.server_version)
    print("Handler.protocol_version >>>", Handler.protocol_version)
    print("MyHandler.server_version >>>", MyHandler.server_version)
    print("MyHandler.protocol_version >>>", MyHandler.protocol_version)

    print("MyHandler.server >>>", MyHandler.server) # ERROR
    print("MyHandler.client_addr >>>", MyHandler.client_addr) # ERROR
    print("httpd.server >>>", httpd.server) # ERROR
except:
    print("ERROR")

try:
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    httpd.socket.close()
