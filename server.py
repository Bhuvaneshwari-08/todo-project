import http.server
import socketserver
import urllib.parse
import os

PORT = 8000
TASK_FILE = 'tasks.txt'

class ToDoHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(post_data)
        task = data.get('task', [''])[0].strip()

        if self.path == '/delete':
            if os.path.exists(TASK_FILE):
                with open(TASK_FILE, 'r') as f:
                    tasks = f.readlines()
                tasks = [t for t in tasks if t.strip() != task]
                with open(TASK_FILE, 'w') as f:
                    f.writelines(tasks)
        elif self.path == '/':
            if task:
                with open(TASK_FILE, 'a') as f:
                    f.write(task + '\n')

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        if self.path == '/tasks':
            if not os.path.exists(TASK_FILE):
                tasks = []
            else:
                with open(TASK_FILE, 'r') as f:
                    tasks = f.readlines()

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(''.join(tasks).encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), ToDoHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
