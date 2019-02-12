import socket
import re
import threading
import os
import mimetypes
import datetime
import ssl
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import to_bytes
import traceback
import time
import logging
import random
import uuid
import cgi
import hashlib
import string
import subprocess

working_directory = os.path.dirname(os.path.realpath(__file__))
data_directory = os.path.dirname(os.path.realpath(__file__)) + '\data'
print("Working Dir: " + working_directory)
print("Data Dir: " + data_directory)
port_to_serve = 25565
web_name = 'localhost'

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        start = time.time()
        print("FILE BEING POSTED?: " + self.path)
        form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})

        self.send_response(200)
        self.end_headers()
        f = open(data_directory + '\\' + 'img', 'wb')
        f.write(form['imagedata'].value)
        f.close()
        
        output = subprocess.check_output('python C:\\Users\\camposbotellob\\Box\\School\\SoftwareArchitecture\\se3810-lab7\\model\\tutorials\\image\\imagenet\\classify_image.py --image_file \"' + data_directory + '\\' + 'img' + "\"", shell=True)
        #os.remove(data_directory + '/' + form['filename'].value)
        self.wfile.write(output + str.encode("\nResponse Time: " + str(time.time() - start) + "\n"))        
        os.remove(data_directory + '\\' + form['filename'].value)
        return

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        print("path:" + self.path + "\n")
        if self.path == '/':
            self.wfile.write(open(data_directory + '\\index.html', 'rb').read())
        else:
            self.wfile.write(open(data_directory + self.path.replace('/', "\\"), 'rb').read())
        return
	
def main():
    try:
        httpd = http.server.HTTPServer((web_name, port_to_serve), RequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=working_directory+'\\server.pem', server_side=True)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting off the server...')
        httpd.socket.close()

main()
