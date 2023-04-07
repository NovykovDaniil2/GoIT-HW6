from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
from threading import Thread
import socket
import pathlib
import json
import logging


BASE_DIR = pathlib.Path()
DYNAMIC_PAGES = {'/' : 'index.html', '/message.html' : 'message.html'}
SUCCESSFUL_CODE = 200
SOCKET_IP = '127.0.0.1'
SOCKET_PORT = 5000
SERVER_IP = '0.0.0.0'
SERVER_PORT = 3000
BUFFER = 1024


class HTTPHandler(BaseHTTPRequestHandler):


    def do_GET(self):

        url = urllib.parse.urlparse(self.path)
        if url.path in DYNAMIC_PAGES:
            self.send_html(DYNAMIC_PAGES[url.path])
        elif pathlib.Path().joinpath(url.path[1:]).exists():
            self.send_static()
        else:
            self.send_html('error.html')

            
    def send_static(self):

        self.send_response(SUCCESSFUL_CODE)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


    def send_html(self, filename, status = SUCCESSFUL_CODE):

        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


    def do_POST(self):

        body = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_socket(body)
        self.send_html('message.html')


def send_data_to_socket(body):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body, (SOCKET_IP, SOCKET_PORT))
    client_socket.close()


def save_data(body):

    try:
        body = urllib.parse.unquote_plus(body.decode())
        user_data = {key : value for key, value in [i.split('=') for i in body.split('&')]}
        file_path = BASE_DIR.joinpath('storage', 'data.json')
        with open(file_path, 'r', encoding='utf-8') as fd:
            saved_data = json.load(fd)
        with open(file_path, 'w', encoding='utf-8') as fd:
            saved_data.append(user_data)
            json.dump(saved_data, fd, ensure_ascii=False, indent=4)   
    except ValueError as err:
        logging.error(f' Error: " {err} " has been caught at the time of saving {user_data}')
    except OSError as err:
        logging.error(f' Error: " {err} " has been caught at the time of saving {user_data}')


def run_server(server_class=HTTPServer, handler_class=HTTPHandler):

    server_address = (SERVER_IP, SERVER_PORT)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server(ip, port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            body = server_socket.recv(BUFFER)
            save_data(body)
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s', handlers=[logging.StreamHandler()])

    if not pathlib.Path('storage/data.json').exists():
        with open('storage/data.json', 'w+') as fd:
            json.dump([], fd)

    th_server = Thread(target=run_server)
    th_server.start()
    th_socket= Thread(target=run_socket_server(SOCKET_IP, SOCKET_PORT))
    th_socket.start()
