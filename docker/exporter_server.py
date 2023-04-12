import http.server      # Our http server handler for http requests
import socketserver     # Establish the TCP Socket connections
from scraper_tm_intervals import TMScrapeMetrics, TMScrapeIndex

PORT = 9095


class IndexHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        # self.send_header("Content-length", len(TMScrapeMetrics().__repr__()))
        self.end_headers()
        self.wfile.write(TMScrapeIndex().__repr__())
        # self.path = 'static/index.html'
        # return http.server.SimpleHTTPRequestHandler.do_GET(self)


class MetricsHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(TMScrapeMetrics().__repr__())


index_page = IndexHttpRequestHandler
metrics_page = MetricsHttpRequestHandler

with socketserver.TCPServer(("localhost", PORT), metrics_page) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()
