#!/usr/bin/env python
#
#Pudoku, a sudoku web interface
#Copyright (c) 2011, Sina Samavati
#Licensed under the BSD License http://www.opensource.org/licenses/BSD-3-Clause


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from sudokulib import sudoku
import mimetypes
import os
import platform
import sys
import time
# import webbrowser

class Pudoku(BaseHTTPRequestHandler) :

    #Detect pathes and send response to the http server
    def do_GET(self) :
        if self.path == '/' :
            self.template(body=file('layouts/index.html').read())

        #Generate the game with a level
        elif self.path.lower() == '/easy' :
            self.template(title='Easy - Pudoku', body=self.pudo())

        elif self.path.lower() == '/medium' :
            self.template(title='Pudoku - Medium', body=self.pudo(1))

        elif self.path.lower() == '/hard' :
            self.template(title='Pudoku - Hard', body=self.pudo(2))

        #Put content of the license into the main layout
        elif self.path.lower() == '/license' :
            self.template(title='License', body=file('layouts/license.html').read())

        #Recognize the result of the game (either win or lose)
        elif '?pudo=' in self.path :
            x = self.path[self.path.find('?')+1:].replace('pudo=', '').replace('&', '')
            inputs = [int(y) for y in x]

            if inputs == self.solution :
                self.template(title='Win',
                              body='<h2>Congratulations!</h2><center><p>You won the game!</p></center>')

            else :
                self.template(title='Lose',
                              body='<h2>Sorry!</h2><center><p>You haven\'t been able to win the game</p></center>')

        else :
            try :
                self.content = file(self.path[1:]).read() if os.path.isfile(self.path[1:]) else file('%s/index.html' % self.path[1:]).read() 
                self.sendResponse(mimetypes.guess_type(self.path[1:])[0] if os.path.isfile(self.path[1:]) else 'text/html')

            except :
                self.content = "<h1>404</h1>"
                self.sendResponse()


    #Generate the template
    def template(self, Type='text/html', title='Pudoku', body=None) :
        self.content = file('layouts/main.html').read()
        self.content = self.content % {'title' : title,
                                       'content': body}
        self.sendResponse(Type)


    #Send a response to the http server
    def sendResponse(self, Type='text/html') :
        self.send_response(200)
        self.send_header('content-type', '%s' % Type)
        self.end_headers()
        self.wfile.write(self.content)


    #Generate a sudoku
    def pudo(self, difficulty=0) :
        pu = sudoku.Sudoku(difficulty=difficulty)
        do = [str(e) for e in pu.masked_grid]
        ku = ['<center><form action="" method="GET">\n']
        l = [i*27 for i in xrange(4)]
        c = 0

        for n in do :

            if c in l :
                ku.append('%s\n<br /> %s <br />\n' % ('|' if c != 0 else '', '-' * 90))

            if c % 9 == 0 and c not in l :
                ku.append('|\n<br />\n')
                
            if c % 3 == 0 :
                ku.append('|')

            ku.append('<input align="top" type="text" %s value="%s" ' \
                       'name="pudo" maxlength="1" style="width:25px" />\n' \
                            % ('readonly="readonly"' if n else '', n))

            c += 1

        ku.append('|\n<br /> %s <br />' % ('-' * 90))
        ku.append('\n<br /><br />\n<input type="submit" value="Submit" /></form></center>')
        Pudoku.pudoku = ' '.join(ku)
        Pudoku.solution = pu.solution
        return self.pudoku


def main() :
    parser = OptionParser(description='Pudoku is a sudoku web interface', 
                          version='Pudoku 1.0')
    parser.add_option('--host', type='str', default='localhost', 
                      help='\tHost to import from')
    parser.add_option('--port', type='int', default=5000,
                      help='\tPort to import from')

    help_context = {'--version' : '\tDisplay current version',
                    '--help' : '\tDisplay this help message and exit'}

    #A simple hack
    for counter in xrange(len(parser.option_list)) :
        option = parser.option_list[counter].get_opt_string()
        if option in help_context :
            parser.option_list[counter].help = help_context[option]

    opt  = parser.parse_args()[0]
    host = opt.host
    port = opt.port
    serverClass = HTTPServer
    httpd = serverClass((host, port), Pudoku)

    print '[%s]\tpython %s [%s-%s]' % (time.strftime("%Y-%m-%d %H:%M:%S"), platform.python_version(), platform.system(), platform.machine())
    time.sleep(0.5)
    print '[%s]\tHTTPServer pid:%d %s:%d' % (time.strftime("%Y-%m-%d %H:%M:%S"), os.getpid(), host, port)
    time.sleep(0.5)

    #webbrowser.open('http://%s:%d' % (host, port), new=0, autoraise=True) #it will open a new tab/window in your default web browser
    #you can enable the above code if you want it

    try :
        #Just have a look at the below (It's recognizable)
        httpd.serve_forever()

    except KeyboardInterrupt :
        #Press <Ctrl>+c for when you want to stop it
        sys.stdout.write('\b\b')
        sys.stdout.flush()
        print '[%s]\tgoing to shut down ...' % time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(0.5)
        httpd.server_close()
    

if __name__ == '__main__' :
    main()

#I hope it's useful
