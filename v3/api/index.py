# Python 3 server example -> https://pythonbasics.org/webserver/
from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import urllib.parse

hostName = "localhost"
serverPort = 8000


class MyServer(BaseHTTPRequestHandler):

    # check for get request
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        # return all products
        if url.path == '/products':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-type", "application/json")
            self.end_headers()
            # Connecting to sqlite
            # connection object
            connection = sqlite3.connect('database/stickers.db')

            # cursor object
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products")
            # get all records
            rows = cursor.fetchall()

            # for row in rows:
                # print(row)

            # Close the connection
            connection.close()
            json_data = json.dumps(rows)

            # Send the JSON data as the response
            self.wfile.write(json_data.encode())
            # return 1 product -> /product?name=product_1
        elif url.path == '/product':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # dict -> new dictionary initialized with the name=value pairs
            url_query = dict(urllib.parse.parse_qsl(url.query))
            product_name = ''
            # if the existence of a key in a dict
            if 'name' in url_query:
                product_name = url_query['name']
            if product_name == '':
                json_data = json.dumps('{error: true,msg: "Error empty product name!"}')
                self.wfile.write(json_data.encode())
                return 0
            # connection object
            connection = sqlite3.connect('database/stickers.db')

            # cursor object
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products where productName= '"+product_name+"'")
            # get one row
            row = cursor.fetchone()

            # Close the connection
            connection.close()
            json_data = json.dumps(row)

            # Send the JSON data as the response
            self.wfile.write(json_data.encode())
        else:
            self.path = '/index.html'
            file_to_open = open('index.html').read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))


if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
