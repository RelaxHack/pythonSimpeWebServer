import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleServer(BaseHTTPRequestHandler):
    def do_get(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Send welcome page
            message = """
            <html>
            <head>
            <title>Welcome!</title>
            </head>
            <body>
            <h1>Hi!</h1>
            <a href="/download">Download a file</a>
            </body>
            </html>
            """
            self.wfile.write(message.encode('utf-8'))

        elif self.path == '/download':
            # Determine the path to the download file
            file_path = 'config\\fileToDownload.txt'  # Replace with the path to your file on your computer

            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                self.end_headers()

                # Sending the contents of a file in parts
                with open(file_path, 'rb') as file:
                    chunk = file.read(4096)
                    while chunk:
                        self.wfile.write(chunk)
                        chunk = file.read(4096)
            else:
                self.send_error(404, 'File not found')

        else:
            self.send_error(404, 'Page not found')


def run_server():
    host = 'localhost'
    port = 8000

    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleServer)
    print(f'Server hosted on {host}:{port}')
    httpd.serve_forever()


run_server()
