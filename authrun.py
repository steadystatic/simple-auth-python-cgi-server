import CGIHTTPServer
import SocketServer
import os
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print "send header"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        # User:pass base64 encoded, default admin:admin
        elif self.headers.getheader('Authorization') == 'Basic YWRtaW46YWRtaW4=':
            self.do_HEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('Authenticated')
            self.wfile.write('.........')
            self.wfile.write('Deploying!')
            os.system('touch logfile.log')
            os.system('sh test.sh')
            subprocess.call('tail -f logfile.log', shell=True, executable='/bin/sh')
            print "Done"
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('Not Authenticated')
            pass

httpd = SocketServer.TCPServer(("", 9012), Handler)

httpd.serve_forever()

if __name__ == '__main__':
    main()
