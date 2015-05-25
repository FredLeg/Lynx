#! C:\python34\python

import sys
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer

if sys.argv[1:]: port = int(sys.argv[1])
else:            port = 80

def expl(H):
    R = ''
    for item in H:
        R += "<br/> -> " +  str(item) +" :"+ str(H[item])
    return R

def sub(headers):
    # Il faut modifier: C:\Windows\System32\drivers\etc\hosts
    # exemple: 127.0.0.1      test.localhost
    h_lst = headers['Host'].split('.')
    if h_lst[-1]=='localhost': tmp = h_lst[:-1] 
    else:                      tmp = h_lst[:-2]
    return '.'.join(tmp)

class MyHandler(SimpleHTTPRequestHandler):

    def __init__(self,req,client_addr,server):
        SimpleHTTPRequestHandler.__init__(self,req,client_addr,server)

    def do_GET(self):
        page_text = ""\
                  + "server_version: "+ self.server_version +"<br/>"\
                  + "sys_version: "+ self.sys_version +"<br/>"\
                  + "protocol_version: "+ self.protocol_version +"<br/>"\
                  + "version_string(): "+ str(self.version_string()) +"<br/>"\
                  + "address_string(): "+ self.address_string() +"<br/>"\
                  + "path: "+ self.path +"<br/>"\
                  + "command: "+ self.command +"<br/>"\
                  + "headers: "+ expl(self.headers) +"<br/>"\
                  + "server.server_name: "+ self.server.server_name +"<br/>"\
                  + "sub(headers['Host']): "+ sub(self.headers) +"<br/>"\
                  + "server.server_port: "+ str(self.server.server_port) +"<br/>"\
                  + "server.socket.getsockname(): "+ str(self.server.socket.getsockname()) +"<br/>"\
                  + "responses: "+ expl(self.responses) +"<br/>"
#Err                  + self.client_address +"<br/>"\
#Err                  + str(self.headers.getheaders('referer')) +"<br/>"\
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len( page_text ))
        self.end_headers()
        self.wfile.write( page_text.encode("utf-8") )

try:
    server_address = ('myserver.io', port)
    httpd = HTTPServer(server_address, MyHandler)
    print("httpd.server_name >>>", httpd.server_name)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    httpd.socket.close()
else:
    input()
