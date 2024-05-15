import json
import http.server
import socketserver
from controllers.user_controller import register_user, login_user
from controllers.product_controller import (
    create_product,
    get_all_products,
    modify_product,
    remove_product,
)

PORT = 8080


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/v1":
            self.handle_root()
        elif self.path.startswith("/v1/product/get"):
            self.handle_get_products()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path.startswith("/v1/auth/register"):
            self.handle_register()
        elif self.path.startswith("/v1/auth/login"):
            self.handle_login()
        elif self.path.startswith("/v1/auth/logout"):
            self.handle_logout()
        elif self.path.startswith("/v1/product/add"):
            self.handle_post_product()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith("/v1/product/update"):
            self.handle_update_product()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/v1/product/delete"):
            self.handle_delete_product()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_root(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Aplikasi server sudah berhasil dijalankan :D"}
        self.wfile.write(json.dumps(response).encode())

    def handle_register(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        response, status_code = register_user(data)
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_login(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        response, status_code = login_user(data)
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_logout(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Logged out successfully"}
        self.wfile.write(json.dumps(response).encode())

    def handle_get_products(self):
        response, status_code = get_all_products(self.headers)
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_post_product(self):
        response, status_code = create_product(self.headers, self.rfile)
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_update_product(self):
        response, status_code = modify_product(self.headers, self.rfile)
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_delete_product(self):
        response, status_code = remove_product(self.headers, self.rfile)
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port http://127.0.0.1:{PORT}")
    httpd.serve_forever()
