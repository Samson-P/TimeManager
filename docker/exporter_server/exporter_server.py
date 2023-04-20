import http.server      # Our http server handler for http requests
import socketserver     # Establish the TCP Socket connections
from scraper_tm_intervals import TMScrapeMetrics, TMScrapeIndex


EXPORTER_SERVER_PORT = 9090


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case '/metrics':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(TMScrapeMetrics().__repr__())
            case '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(TMScrapeIndex().__repr__())
            case '/main.ico':
                self.path = 'static/main.ico'
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            case _:
                self.send_response(404)

# from urllib.parse import urlparse
# import urllib
# В дальнейшем может понадобиться для парсинга данных GET запроса
# o = urllib.parse.urlparse(self.path)
# print(urllib.parse.parse_qs(o.query))


pages = HttpRequestHandler

with socketserver.TCPServer(("localhost", EXPORTER_SERVER_PORT), pages) as httpd:
    print("HTTP server of TimeManager exporter hosts on port", EXPORTER_SERVER_PORT)
    httpd.serve_forever()
