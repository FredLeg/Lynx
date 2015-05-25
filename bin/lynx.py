# -*- Python -*-
# -*- coding: Latin-1 -*-
#
"""
cdApp - Search function for the cdServer demo.
"""
#
#This file is put into the public domain.
#
########################################
# Import needed python modules
########################################

import SimpleHTTPServer, os, string, sys, time, urllib


########################################
# subroutines
########################################

def read_db(filename):
    """
    Read in the database file.
    Returns a list of fortunes.
    """
    lines = open(filename,"r").readlines()
    fortunes = []
    fortune = ""
    for line in lines:
        # "%" at pos 1 of a line is the delimiter
        if line[0:1] == "%":
            fortunes.append(fortune)
            fortune = ""
        else:
            fortune += line
    if fortune:
        fortunes.append(fortune)
    return (fortunes)


def makepage(cont="duh...", title="(cdApp -- untitled)"):
    """format a page from template"""
    global template
    page = template[:]
    page = string.replace(page, "<!--@@search-->", 'Search database')
    page = string.replace(page, "<!--@@exit-->", '<a href="%sexit_">Quitter</a>' % prefix)
    page = string.replace(page, "@@cont", cont)
    page = string.replace(page, "@@title", title)
    return myconv(page)


def myconv(s):
    """HTML-encode special characters"""
    for k in html_ent.keys():
        s = string.replace(s,k,html_ent[k])
    return s


def markup(text, pos, length):
    """markup rearch result"""
    return text[0:pos] + "<strong>" + text[pos:pos+length] + "</strong>" + text[pos+length:]


########################################
# initialize App
########################################

# cdServer checks this variable after each request
# to see if cdApp likes to terminate
end_flag = None

# cdServer displays the following string on console
# if initialization succeeds
version="demoCdApp version 0.5"

# all requests for our special functions start with "/func/". Change to your taste.
prefix = "/func/"
static = "/inc/"

# form for new query
form = """
<form method="get" action="query">
<table>
<tr>
   <td>Query:&nbsp;&nbsp;</td>
   <td><input type="text" size="30" name="pattern" value="%s"></td>
   <td><input type="submit" value="start"></td>
   </tr>
</table>
</form>
"""

# html entities
html_ent={
    '�' : '&iexcl;',
    '�' : '&cent;',
    '�' : '&pound;',
    '�' : '&yen;',
    '�' : '&sect;',
    '�' : '&copy;',
    '�' : '&ordf;',
    '�' : '&laquo;',
    '�' : '&not;',
    '�' : '&shy;',
    '�' : '&reg;',
    '�' : '&macr;',
    '�' : '&deg;',
    '�' : '&plusmn;',
    '�' : '&sup2;',
    '�' : '&sup3;',
    '�' : '&micro;',
    '�' : '&para;',
    '�' : '&middot;',
    '�' : '&sup1;',
    '�' : '&ordm;',
    '�' : '&raquo;',
    '�' : '&iquest;',
    '�' : '&Agrave;',
    '�' : '&Aacute;',
    '�' : '&Acirc;',
    '�' : '&Atilde;',
    '�' : '&Auml;',
    '�' : '&Aring;',
    '�' : '&AElig;',
    '�' : '&Ccedil;',
    '�' : '&Egrave;',
    '�' : '&Eacute;',
    '�' : '&Ecirc;',
    '�' : '&Euml;',
    '�' : '&Igrave;',
    '�' : '&Iacute;',
    '�' : '&Icirc;',
    '�' : '&Iuml;',
    '�' : '&ETH;',
    '�' : '&Ntilde;',
    '�' : '&Ograve;',
    '�' : '&Oacute;',
    '�' : '&Ocirc;',
    '�' : '&Otilde;',
    '�' : '&Ouml;',
    '�' : '&times;',
    '�' : '&Oslash;',
    '�' : '&Ugrave;',
    '�' : '&Uacute;',
    '�' : '&Ucirc;',
    '�' : '&Uuml;',
    '�' : '&Yacute;',
    '�' : '&THORN;',
    '�' : '&szlig;',
    '�' : '&agrave;',
    '�' : '&aacute;',
    '�' : '&acirc;',
    '�' : '&atilde;',
    '�' : '&auml;',
    '�' : '&aring;',
    '�' : '&aelig;',
    '�' : '&ccedil;',
    '�' : '&egrave;',
    '�' : '&eacute;',
    '�' : '&ecirc;',
    '�' : '&euml;',
    '�' : '&igrave;',
    '�' : '&iacute;',
    '�' : '&icirc;',
    '�' : '&iuml;',
    '�' : '&eth;',
    '�' : '&ntilde;',
    '�' : '&ograve;',
    '�' : '&oacute;',
    '�' : '&ocirc;',
    '�' : '&otilde;',
    '�' : '&ouml;',
    '�' : '&divide;',
    '�' : '&oslash;',
    '�' : '&ugrave;',
    '�' : '&uacute;',
    '�' : '&ucirc;',
    '�' : '&uuml;',
    '�' : '&yacute;',
    '�' : '&thorn;',
    '�' : '&yuml;',
}

# read in database and template file

server_root = os.getcwd()
datadir     = os.path.join(server_root,"")
testfile    = os.path.join(datadir, "test.txt")
tfile       = os.path.join(datadir, "index.html") # template.html

import sqlite3
#print(sys.version)
from   collections import namedtuple
def cursor_fields(cur):
    # Formats the return: ( Cursor, namedtuple of cursor's fields )
    print( "### cur.description ", cur.description )
    return((cur,namedtuple('o',[i[0] for i in cur.description])))
##Cursor.executescript ('''DROP TABLE IF EXISTS basic''')
Connect = sqlite3.connect('LYNX.sqlite3')
Cursor = Connect.cursor()
#Cursor.execute('''CREATE TABLE basic(
#  id INTEGER PRIMARY KEY NOT NULL,
#  word text,
#  def text
#)''')
Cursor.execute('SELECT word, definition FROM basic')
cursor,fields = cursor_fields(Cursor)
dbcontent = '';
for row in cursor:
	o = fields._make(row)
	dbcontent += "<p>"+ o.word.encode("utf-8") +" : "+ o.definition.encode("utf-8") +"</p>"
Cursor.close()
Connect.close()


print "Reading page template ..."
template = open(tfile,"r").read()

###print "Reading database ..."
#database = read_db(testfile)
testContent = open(testfile,"r").read()

sfrom = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ����������������������������������' + \
        'abcdefghijklmnopqrstuvwxyz������������������������������������'
sto   = 'abcdefghijklmnopqrstuvwxyzszoyaaaaaaaceeeeiiiidnoooooouuuuyy' + \
        'abcdefghijklmnopqrstuvwxyzsmzosaaaaaaaceeeeiiiidnoooooouuuuyyy'
xlat  = string.maketrans(sfrom,sto)


allowed_hosts = ['127.0.0.1']

def checkACL(host):
    """check if host is allowed to connect (overridden by cdServer)"""
    return host in allowed_hosts

debug = False


################################################################################
# Special Request Handler for HTTP requests to our server
################################################################################

class SimpleHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Complete HTTP server with GET and HEAD requests.

    GET and HEAD also support inline search functions.
    """

    def do_HEAD(self):
        """send headers or forward request to SimpleHTTPServer"""

        if not checkACL(self.client_address[0]):
            self.send_response(403)
        elif self.is_special():
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_HEAD(self)

    def P(self):
        path = self.path
        cmd   = path
        args  = ""
        pos = string.find(cmd,"?")
        if pos >= 0:
            args = cmd[pos+1:]
            cmd = cmd [:pos]
        params = {}
        if args:
            chunks = string.split(args,"&")
            if type(chunks) != type([]):
                chunks = [chunks]
            for chunk in chunks:
                pos = string.find(chunk,"=")
                if pos >=0:
                   params[chunk[:pos]] = chunk[pos+1:]
        self.params = params
        return (path, cmd, params)

    def do_GET(self):
        """Serve a special function or forward request to SimpleHTTPServer"""


        (path, cmd, params) = self.P();
        print( "=======", path )
        print( "=======", cmd )
        print( "=======", self.params.get("doc","") )

        print(">>>>>>>>>>>>>>>>>>>>>>>>> client_address >>>",self.client_address)
        print(">>>>>>>>>>>>>>>>>>>>>>>>> path >>>",self.path)


        if not checkACL(self.client_address[0]):
            self.send_response(403)
            self.wfile.write('Content-type: text/html\n\n')
            self.wfile.write('''<html><body>
                                <h1>Not authorized</h1>
                                <p>Host '%s' is not authorized to access this server.</p>
                                </body></html>''' % self.client_address[0])
        elif self.is_special():
            self.run_special()
        elif self.params.get("doc","")=='database':
            self.run_html()
        elif (self.path[:len(static)] != static):
            self.run_html()
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def is_special(self):
        """Test whether self.path corresponds to a special command and parse request path"""

        # we don't want this function to be run twice (does this really happen?) --
        # so we try to return a variable which is undefined when coming here
        # for the first time ...

        try:
            return self.is_spec
        except AttributeError:
            self.is_spec = 0

        # we analyze the request for several conditions that have to be
        # met in order to qualify as a spacial function
        path = self.path

        if path[:len(prefix)] != prefix:
            return 0

        cmd   = path[len(prefix):]
        args  = ""
        pos = string.find(cmd,"?")
        if pos >= 0:
            args = cmd[pos+1:]
            cmd = cmd [:pos]

        params = {}
        if args:
            chunks = string.split(args,"&")
            if type(chunks) != type([]):
                chunks = [chunks]
            for chunk in chunks:
                pos = string.find(chunk,"=")
                if pos >=0:
                   params[chunk[:pos]] = chunk[pos+1:]

        self.cmd = cmd
        self.params = params
        self.is_spec = 1
        return 1

    def run_html(self):
        """Serve a HTML file

        Read in the file's content and replace @@exit macro with link
        to special exit_ function. If the file can not be found or an
        error occurs (due to a request for a page in an invalid subdirectory)
        the request is forwarded to SimpleHTTPServer.

        The purpose of this extra-handling of html files is obvious:
        in case the file is served off a regular webserver such as apache
        the html file contains the @@exit macro which is commented out
        with html comment signs (<!-- and -->). If being served off
        cdServer with this app then "<!--@@exit-->" is replaced with a
        link to the exit_ function (/func/exit_). Cute, isn't it?
        """

        print ">>>cdApp<<< SimpleHTTPRequestHandler run_html"
        global server_root
        ###Fred: Si l'url est '/':
        if (self.path=='/'): self.path='/index.html'
        ###Fred: fin
        (path, cmd, params) = self.P();
        path = string.replace(cmd[1:],"/", os.sep)
        fname = os.path.join(server_root,path)
        cont = ""
        try:
            cont = open(fname,"r").read()
        except:
            print( "=======", fname, "NON TROUVE" )
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            return
        cont = string.replace(cont, "@@title",   'Manuel')
        cont = string.replace(cont, "<!--@@exit-->",   '<a href="%sexit_">Quitter</a>' % prefix)
        cont = string.replace(cont, "<!--@@search-->", '<a href="%squery">Search database</a>' % prefix)
        
        cont = string.replace(cont, "@@hello", "hello world")
        cont = string.replace(cont, "@@TEST", testContent)
        cont = string.replace(cont, "@@DATABASE", dbcontent)
        #if cont.find('@@DATABASE') != -1:

        self.send_response(200, 'Script output follows')
        self.wfile.write('Content-type: text/html\n\n')
        self.wfile.write(cont)

    def run_special(self):
        """Execute a special function.

        Currently, only "query" and "exit_" are implemented.
        """

        print ">>>cdApp<<< SimpleHTTPRequestHandler run_special"
        self.send_response(200, 'Script output follows')
        self.wfile.write('Content-type: text/html\n\n')

        content = ""
        # ------------------------------------------------
        if self.cmd == "query":
            self.query = self.params.get("pattern","")
            origquery = urllib.unquote_plus(self.query)
            query = string.translate(origquery,xlat)

            content += """<h2>Search database</h2>\n"""
            content += form % (origquery)

            if query == '':
                # no query specified -- prompt user to enter query string
                content += '\n<p><strong>Please enter search pattern</strong></p>\n'
                content = makepage(content, "Search form")
            else:
                # show matches in a tabular list
                content += """<p class="spec"><strong>Search result:</strong></p>\n"""
                nhits = 0

                for fortune in database:
                    test = string.translate(fortune,xlat)
                    pos  = string.find(test,query)
                    if pos >= 0:
                            content += '<hr noshade size="1"><pre>\n' + markup(fortune, pos, len(query)) + "</pre>\n"
                            nhits += 1
                # display hit count
                content += """<hr noshade size="1">\n<strong>%d hit(s)</strong>\n""" % (nhits)
                # advertisement for the Python language...
                content += """<table width="100%"><tr><td align="right" valign="bottom"><a target="python" href="http://www.python.org/">\n"""
                content += """<img src="../images/python.png" alt="[Python Powered]" border="0"></a></td></tr>\n"""
                content += """</table>\n"""
                content = makepage(content, "Search result for '%s'" % origquery)
        # ------------------------------------------------
        elif self.cmd == "exit_":
            global end_flag
            content += "<H2>Bye bye !</H2>"
            end_flag = 1
        # ------------------------------------------------
        else:
            content += "<H2>command '%s' is not (yet) implemented</H2>" % self.cmd

        # finally html-encode and write page
        self.wfile.write(myconv(content))

acl_host = []
acl_net  = []

def setACLs(host,net):
    global acl_host, acl_net
    acl_host = host
    acl_net  = net

################################################################################
# END
################################################################################
