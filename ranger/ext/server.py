import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from multiprocessing.queues import SimpleQueue
import re

class RangerControlHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        request_path = self.path
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        body = self.rfile.read(length)

        call = (request_path, body)
        self.server.queue.put(call)
        self.send_response(200)
    def log_message(self, format, *args):
        return


class RangerControlServer(HTTPServer):
    def __init__(self, fm):
        self.fm = fm
        self.queue = SimpleQueue()
        self.goDie = False
        HTTPServer.__init__(self, ('127.0.0.1', 5964), RangerControlHandler)

    def start(self):
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    def stop(self):
        self.shutdown()

    def process(self):
        self.serve_forever()

    def check_messages(self):
        if self.queue.empty():
            return None
        return self.queue.get()

    def act_on_messages(self):
        msg = self.check_messages()
        if msg == None: return False

        action, arg = msg
        match = re.match(r"/cdtab-(\S+)",action)
        if match != None:
            tab = match.group(1)
            if not (tab in self.fm.tabs):
                self.fm.tab_open(tab, arg)
            else:
                self.fm.tabs[tab].enter_dir(arg)
        elif action == "/cd":
            self.fm.enter_dir(arg)
        elif action == "/cdfirst":
            first_tab = self.fm._get_tab_list()[0]
            self.fm.tabs[first_tab].enter_dir(arg)
        else:
            self.fm.notify("Unknown server command", bad=True)
        return True
        
